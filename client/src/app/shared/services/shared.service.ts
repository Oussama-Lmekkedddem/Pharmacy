import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import {ApiService} from "../../core/service/api.service";
import {User} from "../../features/auth/models/user";
import { Observable, throwError, of } from 'rxjs';
import { catchError, map} from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SharedService {
  private currentUser: any;
  private tokenKey = 'authToken';
  private userKey = 'currentUser';

  private isAuthenticatedSubject = new BehaviorSubject<boolean>(this.hasToken());
  isAuthenticated$ = this.isAuthenticatedSubject.asObservable();


  constructor(
    private apiService: ApiService,
    private router: Router,
  ) {
    this.getCurrentUser();
  }



  logoutUser(): Observable<any> {
    return this.apiService.post('client/logout', {}).pipe(
      map((response: any) => {

        localStorage.removeItem('auth_token');
        localStorage.removeItem(this.tokenKey);
        localStorage.removeItem(this.userKey);
        this.isAuthenticatedSubject.next(false);
        this.clearUser();
        this.router.navigate(['/auth/sign-in']);
        return response;
      }),
      catchError(this.handleError)
    );
  }

  private hasToken(): boolean {
    return !!localStorage.getItem(this.tokenKey);
  }

  clearUser() {
    this.currentUser = null;
    localStorage.removeItem('currentUser');
  }
  getCurrentUser(): Observable<User | undefined> {
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
