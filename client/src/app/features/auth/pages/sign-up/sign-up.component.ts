import { Component} from '@angular/core';
import { Router } from '@angular/router';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {NgIf} from "@angular/common";
import {AuthService} from "../../services/auth.service";
@Component({
  selector: 'app-sign-up',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    NgIf
  ],
  templateUrl: './sign-up.component.html',
  styleUrl: './sign-up.component.css'
})
export class SignUpComponent {
  signUpForm: FormGroup;
  errorMessage: string = '';


  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.signUpForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      password_confirmation: ['', Validators.required]
    }, { validators: this.passwordMatchValidator });
  }

  passwordMatchValidator(form: FormGroup) {
    const password = form.get('password')?.value;
    const passwordConfirmation = form.get('password_confirmation')?.value;
    return password === passwordConfirmation ? null : { 'mismatch': true };
  }

  onSubmit(): void {
    if (this.signUpForm.valid) {
      const { name, email, password } = this.signUpForm.value;
      const user: any = {
        name,
        email,
        password
      };

      console.log('User in sing-up:'+ user.name +' '+user.email +' '+user.password);
      this.authService.createUser(user).subscribe({
        next: (response) => {
          console.log('User registered successfully:', response);
          this.router.navigate(['/auth/sign-in']);
        },
        error: (error) => {
          console.error('Error during sign up:', error);
          this.errorMessage = error.error?.message || 'Registration failed.';
        }
      });
    }
  }
}
