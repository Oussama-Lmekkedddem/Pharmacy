import { Component } from '@angular/core';
import {AuthService} from '../../services/auth.service';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [
    ReactiveFormsModule,
  ],
  templateUrl: './forgot-password.component.html',
  styleUrl: './forgot-password.component.css'
})
export class ForgotPasswordComponent {
  signUpForm: FormGroup;
  errorMessage: string = '';

   constructor(
     private fb: FormBuilder,
     private authService: AuthService,
  ) {
    this.signUpForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
    });
  }

  onSendPasswordEmail(): void {
    if (this.signUpForm.valid) {
      const { email} = this.signUpForm.value;

      console.log('User in forg_pass:'+ email );
      this.authService.forgotPasswordUser(email).subscribe({
        next: (response) => {
          this.errorMessage = 'An email has been sent to your inbox. Please check your email.';
          console.log('Send registered successfully:', response);
        },
        error: (error) => {
          this.errorMessage = error.error?.message || 'Operation failed.';
          console.error('Error during forget pass user:', error);
        }
      });
    }
  }
}
