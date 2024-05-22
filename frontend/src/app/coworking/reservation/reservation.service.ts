import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map, shareReplay, tap, Subscription } from 'rxjs';
import {
  Reservation,
  ReservationJSON,
  parseReservationJSON
} from '../coworking.models';
import { RxReservation } from './rx-reservation';

export interface Group {
  gid: number;
  pid: number[];
  date: string;
}

@Injectable({
  providedIn: 'root'
})
export class ReservationService {
  private reservations: Map<number, RxReservation> = new Map();
  public gid: number = 0;

  constructor(private http: HttpClient) {}

  get(id: number): Observable<Reservation> {
    let reservation = this.getRxReservation(id);
    reservation.load();
    return reservation.value$;
  }

  getUserGroup(pid: number) {
    console.log('get user from group');
    return this.http.get<number>(`/api/group/user/${pid}`);
  }

  delete(pid: number) {
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

  cancel(reservation: Reservation) {
    let endpoint = `/api/coworking/reservation/${reservation.id}`;
    let payload = { id: reservation.id, state: 'CANCELLED' };
    return this.http.put<ReservationJSON>(endpoint, payload).pipe(
      map(parseReservationJSON),
      tap((reservation) => {
        let rxReservation = this.getRxReservation(reservation.id);
        rxReservation.set(reservation);
      })
    );
  }

  confirm(reservation: Reservation) {
    let endpoint = `/api/coworking/reservation/${reservation.id}`;
    let payload = { id: reservation.id, state: 'CONFIRMED' };
    return this.http.put<ReservationJSON>(endpoint, payload).pipe(
      map(parseReservationJSON),
      tap((reservation) => {
        let rxReservation = this.getRxReservation(reservation.id);
        rxReservation.set(reservation);
      })
    );
  }

  checkout(reservation: Reservation) {
    let endpoint = `/api/coworking/reservation/${reservation.id}`;
    let payload = { id: reservation.id, state: 'CHECKED_OUT' };
    return this.http.put<ReservationJSON>(endpoint, payload).pipe(
      map(parseReservationJSON),
      tap((reservation) => {
        let rxReservation = this.getRxReservation(reservation.id);
        rxReservation.set(reservation);
      })
    );
  }

  private getRxReservation(id: number): RxReservation {
    let reservation = this.reservations.get(id);
    if (reservation === undefined) {
      let loader = this.http
        .get<ReservationJSON>(`/api/coworking/reservation/${id}`)
        .pipe(
          map(parseReservationJSON),
          shareReplay({ windowTime: 1000, refCount: true })
        );
      reservation = new RxReservation(loader);
      this.reservations.set(id, reservation);
    }
    return reservation;
  }
}
