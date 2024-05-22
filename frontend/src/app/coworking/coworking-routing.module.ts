import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CoworkingPageComponent } from './coworking-home/coworking-home.component';
import { AmbassadorPageComponent } from './ambassador-home/ambassador-home.component';
import { ReservationComponent } from './reservation/reservation.component';
import { SliderComponent } from './slider/slider.component';
import { GroupComponent } from './group/group.component';
import { SuccessComponent } from './success/success.component';

const routes: Routes = [
  CoworkingPageComponent.Route,
  ReservationComponent.Route,
  AmbassadorPageComponent.Route,
  {
    path: 'group-reservation',
    component: SliderComponent,
    title: 'Group Reservation'
  },
  {
    path: 'group-reservation/group-details',
    component: GroupComponent,
    title: 'Group Details'
  },
  {
    path: 'group-reservation/group-details/success',
    component: SuccessComponent,
    title: 'Group Reservation Success'
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CoworkingRoutingModule {}
