import { AsyncPipe, CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { CoworkingRoutingModule } from './coworking-routing.module';
import { CoworkingPageComponent } from './coworking-home/coworking-home.component';
import { AmbassadorPageComponent } from './ambassador-home/ambassador-home.component';
import { MatCardModule } from '@angular/material/card';
import { CoworkingReservationCard } from './widgets/coworking-reservation-card/coworking-reservation-card';
import { MatDividerModule } from '@angular/material/divider';
import { CoworkingDropInCard } from './widgets/dropin-availability-card/dropin-availability-card.widget';
import { MatListModule } from '@angular/material/list';
import { CoworkingHoursCard } from './widgets/operating-hours-panel/operating-hours-panel.widget';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { ReservationComponent } from './reservation/reservation.component';
import { FormsModule } from '@angular/forms';
import { SliderComponent } from './slider/slider.component';
import { GroupComponent } from './group/group.component';
import { GroupService } from './group.service';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { SuccessComponent } from './success/success.component';

@NgModule({
  declarations: [
    CoworkingPageComponent,
    ReservationComponent,
    AmbassadorPageComponent,
    CoworkingDropInCard,
    CoworkingReservationCard,
    CoworkingHoursCard,
    SliderComponent,
    GroupComponent,
    SuccessComponent
  ],
  imports: [
    CommonModule,
    CoworkingRoutingModule,
    MatCardModule,
    MatDividerModule,
    MatListModule,
    MatExpansionModule,
    MatButtonModule,
    MatTableModule,
    FormsModule,
    HttpClientModule,
    ReactiveFormsModule,
    AsyncPipe
  ],
  providers: [Location, GroupService]
})
export class CoworkingModule {}
