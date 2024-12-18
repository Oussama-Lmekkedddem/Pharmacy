import { Component } from '@angular/core';
import {AuthService} from '../../services/auth.service';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import { Router } from '@angular/router';

@Component({
  selector: 'app-new-password',
  standalone: true,
  imports: [
    ReactiveFormsModule,
  ],
  templateUrl: './new-password.component.html',
  styleUrl: './new-password.component.css'
})
export class NewPasswordComponent {
   signUpForm: FormGroup;
   errorMessage: string = '';

  constructor(
     private fb: FormBuilder,
     private authService: AuthService,
     private router: Router
  ) {
    this.signUpForm = this.fb.group({
      password: ['', [Validators.required, Validators.minLength(8)]],
      password_confirmation: ['', Validators.required]
    }, { validators: this.passwordMatchValidator });
  }

  passwordMatchValidator(form: FormGroup) {
    const password = form.get('password')?.value;
    const passwordConfirmation = form.get('password_confirmation')?.value;
    return password === passwordConfirmation ? null : { 'mismatch': true };
  }


  onSendNewPassword(): void {
    if (this.signUpForm.valid) {
      const { password } = this.signUpForm.value;

      console.log('User in forg_pass:'+ password);
      this.authService.newPasswordUser(password).subscribe({
        next: (response) => {
          this.router.navigate(['/auth/sign-in']);
          console.log('Send registered successfully:', response);
        },
        error: (error) => {
          console.error('Error during new pass user:', error);
          this.errorMessage = error.error?.message || 'Operation failed.';
        }
      });
    }
  }
}
