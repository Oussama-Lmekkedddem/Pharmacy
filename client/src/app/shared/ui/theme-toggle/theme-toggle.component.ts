import { Component } from '@angular/core';
import {ThemeService} from "../../utils/theme.service";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-theme-toggle',
  standalone: true,
  imports: [
    NgIf
  ],
  templateUrl: './theme-toggle.component.html',
  styleUrl: './theme-toggle.component.css'
})

export class ThemeToggleComponent {
  isDarkMode: boolean;

  constructor(private themeService: ThemeService) {
    this.isDarkMode = this.isCurrentDarkMode();
  }

  toggleTheme() {
    this.themeService.toggleTheme();
    this.isDarkMode = this.isCurrentDarkMode();
  }

  private isCurrentDarkMode(): boolean {
    return localStorage.getItem('color-theme') === 'dark';
  }
}
