import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ThemeService {
  private themeKey = 'color-theme';

  constructor() {
    this.applyTheme();
  }

  private applyTheme() {
    const currentTheme = localStorage.getItem(this.themeKey);
    if (currentTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  toggleTheme() {
    const currentTheme = localStorage.getItem(this.themeKey);
    if (currentTheme === 'dark') {
      document.documentElement.classList.remove('dark');
      localStorage.setItem(this.themeKey, 'light');
    } else {
      document.documentElement.classList.add('dark');
      localStorage.setItem(this.themeKey, 'dark');
    }
    this.applyTheme();
  }
}
