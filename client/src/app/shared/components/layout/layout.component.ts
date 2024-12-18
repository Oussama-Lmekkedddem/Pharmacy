import { Component } from '@angular/core';
import {NavbarComponent} from "../navbar/navbar.component";
import {MainComponent} from "../main/main.component";
import {SharedService} from "../../services/shared.service";

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [
    NavbarComponent,
    MainComponent
  ],
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.css'
})
export class LayoutComponent {
  constructor(private sharedService: SharedService) {}

}
