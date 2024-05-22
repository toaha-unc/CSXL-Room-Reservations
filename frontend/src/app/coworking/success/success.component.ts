import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { GroupService } from '../group.service';
import { Location } from '@angular/common';

@Component({
  selector: 'app-success',
  templateUrl: './success.component.html',
  styleUrls: ['./success.component.css']
})
export class SuccessComponent implements OnInit {
  currentValue: number = 0;
  constructor(
    private route: ActivatedRoute,
    private groupService: GroupService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.currentValue = this.groupService.getCurrentValue();
  }

  goBack(): void {
    this.location.back();
  }
}
