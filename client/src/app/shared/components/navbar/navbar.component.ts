import { Component, OnInit  } from '@angular/core';
import {ThemeToggleComponent} from "../../ui/theme-toggle/theme-toggle.component";
import {SharedService} from "../../services/shared.service";
import {NgIf} from "@angular/common";
import {Router} from "@angular/router";

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    ThemeToggleComponent,
    NgIf,
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent implements OnInit{

  isUserLoggedIn: boolean = false;

  constructor(
    private sharedService: SharedService,
  ) {}

  ngOnInit(): void {
    this.checkLoginStatus();
  }

  signOut(): void {
    this.sharedService.logoutUser();
    this.isUserLoggedIn = false;
  }

  checkLoginStatus(): void {
    this.isUserLoggedIn = !!localStorage.getItem('token');
  }

}
