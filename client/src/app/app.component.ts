import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {ThemeToggleComponent} from './shared/ui/theme-toggle/theme-toggle.component';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'pharmacy';
}
