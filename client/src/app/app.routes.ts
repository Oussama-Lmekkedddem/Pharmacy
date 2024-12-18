import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadChildren: () => import('./features/pharmacy/pharmacy.module').then(m => m.PharmacyModule),
    // canActivate: [AuthGuard]
  },
   {
    path: 'auth',
    loadChildren: () => import('./features/auth/auth.module').then(m => m.AuthModule),
  },
  {
    path: 'error',
    loadChildren: () => import('./features/error/error.module').then(m => m.ErrorModule),
  },
  { path: '**', redirectTo: '/error' },
];
