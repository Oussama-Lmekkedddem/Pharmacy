import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {SignUpComponent} from "./pages/sign-up/sign-up.component";
import {ForgotPasswordComponent} from "./pages/forgot-password/forgot-password.component";
import {NewPasswordComponent} from "./pages/new-password/new-password.component";
import {SignInComponent} from "./pages/sign-in/sign-in.component";

const routes: Routes = [
  { path: 'forgot-password', component: ForgotPasswordComponent },
  { path: 'new-password', component: NewPasswordComponent },
  { path: 'sign-in', component: SignInComponent },
  { path: 'sign-up', component: SignUpComponent },
  { path: '', redirectTo: 'sign-in', pathMatch: 'full' }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthRoutingModule { }
