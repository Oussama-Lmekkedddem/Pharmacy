import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { NgIf } from '@angular/common';
import {AuthService} from "../../services/auth.service";

@Component({
  selector: 'app-sign-in',
  standalone: true,
  imports: [
    FormsModule,
    NgIf,
  ],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css'
})
export class SignInComponent {
  email: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSignIn(): void {
     console.log('User in sing-in:'+ this.email +' '+ this.password);
    this.authService.loginUser(this.email, this.password).subscribe(
      (response) => {
        if (response.message === 'Login successful') {
          this.router.navigate(['/pharmacy']);
        } else {
          this.errorMessage = 'Invalid credentials';
        }
      },
      (error) => {
        this.errorMessage = 'An error occurred during login';
      }
    );
  }
}
