import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {Error400Component} from "./pages/error400/error400.component";
import {Error500Component} from "./pages/error500/error500.component";

const routes: Routes = [
  { path: 'page-not-found', component: Error400Component },
  { path: 'service-error', component: Error500Component },

  { path: '', redirectTo: 'page-not-found', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ErrorRoutingModule { }
