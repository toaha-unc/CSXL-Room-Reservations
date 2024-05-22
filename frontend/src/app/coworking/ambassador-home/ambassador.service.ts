import { Injectable } from '@angular/core';
import { RxReservations } from './rx-reservations';
import { Observable, map } from 'rxjs';
import {
  Reservation,
  ReservationJSON,
  parseReservationJSON
} from '../coworking.models';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class AmbassadorService {
  private reservations: RxReservations = new RxReservations();
  public reservations$: Observable<Reservation[]> = this.reservations.value$;

  constructor(private http: HttpClient) {}

  fetchReservations(): void {
    this.http
      .get<ReservationJSON[]>('/api/coworking/ambassador')
      .subscribe((reservations) => {
        this.reservations.set(reservations.map(parseReservationJSON));
      });
  }

  checkIn(reservation: Reservation): void {
    this.http
      .put<ReservationJSON>(`/api/coworking/ambassador/checkin`, {
        id: reservation.id,
        state: 'CHECKED_IN'
      })
      .subscribe((reservationJson) => {
        this.reservations.updateReservation(
          parseReservationJSON(reservationJson)
        );
      });
  }

  checkOut(reservation: Reservation) {
    this.http
      .put<ReservationJSON>(`/api/coworking/reservation/${reservation.id}`, {
        id: reservation.id,
        state: 'CHECKED_OUT'
      })
      .subscribe((reservationJson) => {
        this.reservations.updateReservation(
          parseReservationJSON(reservationJson)
        );
      });

    this.delete(reservation.users[0].pid);
  }

  cancel(reservation: Reservation) {
    this.http
      .put<ReservationJSON>(`/api/coworking/reservation/${reservation.id}`, {
        id: reservation.id,
        state: 'CANCELLED'
      })
      .subscribe({
        next: (_) => {
          this.reservations.remove(reservation);
        },
        error: (err) => {
          alert(err);
        }
      });

    this.delete(reservation.users[0].pid);
  }

  getUserGroup(pid: number) {
    console.log('get user from group');
    return this.http.get<number>(`/api/group/user/${pid}`);
  }

  delete(pid: number) {
    console.log('outside of delete');
    this.getUserGroup(pid).subscribe({
      next: (gid) => {
        this.http.delete(`/api/group/${gid}`).subscribe({
          next: (response) => {
            console.log('success');
            // Handle successful delete
          },
          error: (error) => {
            console.log(error);
            // Handle error on delete
          }
        });
      },
      error: (error) => {
        console.log(error);
        // Handle error on getUserGroup
      }
    });
  }
}