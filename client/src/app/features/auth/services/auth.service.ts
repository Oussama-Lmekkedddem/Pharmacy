import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import {tap, map, catchError, delay} from 'rxjs/operators';
import {User} from "../models/user";
import {ApiService} from "../../../core/service/api.service";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUser: any;

  private tokenKey = 'authToken';
  private userKey = 'currentUser';

  private isAuthenticatedSubject = new BehaviorSubject<boolean>(this.hasToken());
  isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  constructor(private apiService: ApiService) {}

  private hasToken(): boolean {
    return !!localStorage.getItem(this.tokenKey);
  }
  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  loginUser(email: string, password: string): Observable<any> {
    console.log('User in sing-in s:'+ email +' '+ password);
    return this.apiService.post('client/login', { email, password }).pipe(
      map((response: any) => {
        if (response.token) {
          localStorage.setItem('auth_token', response.token);
          this.currentUser = response.user;
          return response;
        }
        return null;
      }),
      catchError(this.handleError)
  );
  }

  createUser(user: User): Observable<any> {
     console.log('User in sing_up s:'+ user.name +' '+user.email +' '+user.password);
    return this.apiService.post(`client/create`, user).pipe(
      map((response: any) => response),
      catchError(this.handleError)
    );
  }

  forgotPasswordUser(email: string): Observable<any> {
    return this.apiService.post(`forgotPasswordClient`, email).pipe(
      map((response: any) => response),
      catchError(this.handleError)
    );
  }

  newPasswordUser(password: string): Observable<any> {
    return this.apiService.post(`newPasswordClient`, password).pipe(
      map((response: any) => response),
      catchError(this.handleError)
    );
  }


  setCurrentUser(user: any) {
    this.currentUser = user;
    localStorage.setItem('currentUser', JSON.stringify(user));
  }

  getCurrentUser(): Observable<null> {
    if (!this.currentUser) {
      this.currentUser = JSON.parse(localStorage.getItem('currentUser') || 'null');
    }
    return of(this.currentUser); // Return as Observable
  }

  private handleError(error: any) {
    console.error('An error occurred', error);
    const errorMessage = error.error?.message || error.message || 'Something went wrong; please try again later.';
    return throwError(() => new Error(errorMessage));
  }

}
