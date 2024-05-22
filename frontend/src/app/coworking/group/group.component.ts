import { Component, OnInit, OnDestroy } from '@angular/core';
import { Group } from '../group.service';
import {
  FormBuilder,
  FormGroup,
  Validators,
  FormArray,
  ValidatorFn,
  AbstractControl
} from '@angular/forms';
import { GroupService } from '../group.service';
import { Location } from '@angular/common';
import { Router } from '@angular/router';
import { Subject, Observable, forkJoin } from 'rxjs';
import { switchMap, takeUntil } from 'rxjs/operators';
import { Reservation } from '../coworking.models';
import { Profile } from 'src/app/models.module';

@Component({
  selector: 'app-group',
  templateUrl: './group.component.html',
  styleUrls: ['./group.component.css']
})
export class GroupComponent implements OnInit, OnDestroy {
  pidForm: FormGroup;
  currentValue: number;
  submitted = false;
  displayError = false;
  errorMessage = '';
  isValidated = false;
  currentGroup: Group | null = null;
  seatIssue: number = 0;

  private destroy$ = new Subject<void>();
  profiles: Profile[] = [];
  currentProfile = this.groupService.profile;
  numericPids: number[] = [];

  constructor(
    private fb: FormBuilder,
    private location: Location,
    private groupService: GroupService,
    private router: Router
  ) {
    this.currentValue = this.groupService.getCurrentValue();
    this.pidForm = this.fb.group({
      pids: this.fb.array([])
    });

    this.createPIDControls();
  }

  /** Creates form for storing a list of pids.
   * @returns {void}
   */
  ngOnInit(): void {
    this.pidForm
      .get('date')
      ?.valueChanges.pipe(takeUntil(this.destroy$))
      .subscribe(() => {
        // No actions needed here for now
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  /** Adds pids to the pidForm creates in ngOnInit.
   * @returns {void}
   */
  createPIDControls() {
    // Add the currentProfile PID as the first PID by default
    this.pids.push(
      this.fb.control(
        this.currentProfile ? this.currentProfile.pid.toString() : '',
        [
          Validators.required,
          Validators.pattern('\\d{9}'),
          this.uniquePIDValidator()
        ]
      )
    );

    // Add remaining PIDs
    for (let i = 1; i < this.currentValue; i++) {
      this.pids.push(
        this.fb.control('', [
          Validators.required,
          Validators.pattern('\\d{9}'),
          this.uniquePIDValidator()
        ])
      );
    }
  }

  /** Confirms a pid by checking a variety of uniqueness and registered user tests.
   * @returns {void}
   */
  confirmPIDs(): void {
    this.submitted = true;
    this.displayError = false;
    this.errorMessage = '';
    this.isValidated = false;
    this.numericPids = [];
    this.seatIssue = 0;

    if (this.pidForm.valid) {
      this.pids.controls.forEach((control) => {
        const pid = parseInt(control.value, 10);
        if (!isNaN(pid)) {
          this.numericPids.push(pid);
        }
      });

      // Check if any of the users are in a reservation
      this.groupService
        .checkUsersInReservations(this.numericPids)
        .pipe(
          switchMap((response) => {
            if (response !== 'No users in a reservation') {
              this.displayError = true;
              this.errorMessage = response; // The response indicating that a user is in a reservation
              throw new Error(response);
            }

            // Continue with existing logic if no users are in a reservation
            this.isValidated = true;

            // Call the create method in GroupService with the PIDs
            return this.groupService.create(this.numericPids);
          }),
          switchMap((group) => {
            console.log('Group created:', group);
            return this.groupService.groupExists();
          }),
          switchMap((exists) => {
            if (!exists) {
              throw new Error('Group does not exist');
            }
            const profileRequests = this.numericPids.map((pid) =>
              this.groupService.getProfileByPid(pid)
            );
            return forkJoin(profileRequests);
          }),
          switchMap((profiles) => {
            console.log('Profiles fetched:', profiles);
            this.profiles = profiles;
            this.seatIssue = 1;
            return this.groupService.draftReservation(this.profiles);
          }),
          takeUntil(this.destroy$)
        )
        .subscribe({
          next: (reservation) => {
            console.log('Reservation drafted:', reservation);
            this.router.navigate(['/coworking']);
          },
          error: (err) => {
            this.displayError = true;
            this.errorMessage = err.error.detail;
            if (
              err.message ==
                'Http failure response for http://localhost:1560/api/coworking/reservation: 422 Unprocessable Entity' &&
              this.seatIssue == 1
            ) {
              this.errorMessage = 'Not enough seats available for all users';
              if (this.currentProfile?.pid !== undefined) {
                this.groupService.delete(this.currentProfile.pid);
              }
            }
            this.isValidated = false;
            console.error('Error in process:', err);
          }
        });
    } else {
      console.log('Form is invalid:', this.pidForm.errors);
    }
  }

  /** Goes back to the previous (slider) page.
   * @returns {void}
   */
  goBack(): void {
    this.groupService.setCurrentValue(2);
    this.location.back();
  }

  /** A method that insures each pid is unique in the form.
   * @returns {ValidatorFn}
   */
  uniquePIDValidator(): ValidatorFn {
    return (control: AbstractControl): { [key: string]: any } | null => {
      const index = this.pids.controls.indexOf(control);
      const values = this.pids.value;

      if (
        values.some(
          (val: string, idx: number) => idx !== index && val === control.value
        )
      ) {
        return { uniquePID: true };
      }
      return null;
    };
  }

  /** Returns a list of pids as a FormArray.
   * @returns {FormArray}
   */
  get pids(): FormArray {
    return this.pidForm.get('pids') as FormArray;
  }
}
