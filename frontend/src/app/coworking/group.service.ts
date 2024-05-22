import { AuthenticationService } from '../authentication.service';
import {
  Observable,
  Subscription,
  ReplaySubject,
  Subject,
  catchError,
  map,
  of,
  tap
} from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Injectable, OnDestroy } from '@angular/core';
import {
  CoworkingStatus,
  CoworkingStatusJSON,
  Reservation,
  ReservationJSON,
  ReservationRequest,
  SeatAvailability,
  parseCoworkingStatusJSON,
  parseReservationJSON
} from './coworking.models';
import { ProfileService } from '../profile/profile.service';
import { Profile } from '../models.module';
import { RxCoworkingStatus } from './rx-coworking-status';

const ONE_HOUR = 60 * 60 * 1000;

export interface User {
  id: number;
  pid: number;
  onyen: string;
  first_name: string;
  last_name: string;
  email: string;
  pronouns: string;
  github: string;
  github_id: null;
  github_avatar: null;
}

export interface Group {
  gid: number;
  pid: number[];
  date: string;
}

@Injectable({
  providedIn: 'root'
})
export class GroupService {
  private group: Subject<Group | undefined> = new ReplaySubject(1);
  public group$: Observable<Group | undefined> = this.group.asObservable();
  seats: SeatAvailability[] = [];
  profiles: Profile[] = [];
  gid: number = 0;

  public profile: Profile | undefined;
  private profileSubscription!: Subscription;

  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected profileSvc: ProfileService
  ) {
    this.profileSubscription = this.profileSvc.profile$.subscribe(
      (profile) => (this.profile = profile)
    );
  }

  private currentValue: number = 2;

  /** Sets slider value
   * @returns {void}
   */
  setCurrentValue(value: number): void {
    this.currentValue = value;
  }

  /** Returns the value that was set by the slider in `SetCurrentValue`.
   * @returns {number}
   */
  getCurrentValue(): number {
    return this.currentValue;
  }

  /** Creates a new group of user and adds them to database using HTTP post request.
   * @returns {Observable<Group>}
   */
  create(pids: number[]): Observable<Group> {
    return this.http
      .post<Group>('/api/group', pids)
      .pipe(tap((group) => this.group.next(group)));
  }

  /** Returns the group id of the user entered using HTTP get request.
   * @returns {Observable<number>}
   */
  getUserGroup(pid: number) {
    console.log('get user from group');
    return this.http.get<number>(`/api/group/user/${pid}`);
  }

  /** Delete a group based on a pid (pid associates to their group), calls HTTP delete request.
   * @returns {void}
   */
  delete(pid: number) {
    this.getUserGroup(pid).subscribe({
      next: (gid) => {
        this.http.delete(`/api/group/${gid}`).subscribe({
          next: (response) => {
            console.log('success');
          },
          error: (error) => {
            console.log(error);
          }
        });
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  /** Returns boolean based on if group exists or not using the backend HTTP get request.
   * @returns {Observable<boolean>}
   */
  groupExists(): Observable<boolean> {
    return this.http.get<Group[]>('/api/group').pipe(
      map((groups) => groups.length > 0),
      catchError(() => of(false)) // If error, assume no group exists.
    );
  }

  /** Returns a users profile based off of entered pid using back HTTP get request.
   * @returns {Observable<Profile>}
   */
  getProfileByPid(pid: number): Observable<Profile> {
    return this.http.get<Profile>(`/api/profile/user?pid=${pid}`);
  }

  /** Returns a drafted reservation designed for group reservations using the backend HTTP post request.
   * @returns {Observable<Reservation>}
   */
  draftReservation(users: Profile[]): Observable<Reservation> {
    if (this.profile === undefined) {
      throw new Error('Only allowed for logged in users.');
    }

    // Prepare the reservation request with users and empty seats
    const reservationRequest: ReservationRequest = {
      users: users,
      seats: this.seats, // Empty array as the backend assigns seats automatically
      start: new Date(), // Or any other logic to define the start time
      end: new Date(new Date().getTime() + 2 * ONE_HOUR) // End time after 2 hours
    };

    return this.http
      .post<ReservationJSON>('/api/coworking/reservation', reservationRequest)
      .pipe(map(parseReservationJSON));
  }

  /** Returns a checked in group based off of pids given using the backend HTTP post request.
   * @returns {Observable<string>}
   */
  checkUsersInReservations(pids: number[]): Observable<string> {
    return this.http.post<string>('/api/coworking/reservation/check', { pids });
  }
}
