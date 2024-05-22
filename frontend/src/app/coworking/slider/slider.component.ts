import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { GroupService, User } from '../group.service';
import { Router } from '@angular/router';
import { of } from 'rxjs/internal/observable/of';
import { catchError, map } from 'rxjs/operators';
import { Observable } from 'rxjs';

// Attempted to add a angular mat slider but it wasnt functional, future implementation?
@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.css']
})
export class SliderComponent {
  currentValue: number = 2;

  updateValue(value: string): void {
    this.currentValue = Number(value);
    this.groupService.setCurrentValue(this.currentValue);
  }
  constructor(
    private location: Location,
    private groupService: GroupService,
    private router: Router
  ) {}
  goBack(): void {
    this.groupService.setCurrentValue(2);
    this.location.back();
  }
  onNavigate() {
    this.updateValue(String(this.currentValue));
    this.router.navigateByUrl('/coworking/group-reservation/group-details');
  }
}
