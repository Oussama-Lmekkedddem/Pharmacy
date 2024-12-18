import { Component } from '@angular/core';
import {SharedService} from "../../services/shared.service";
import {RouterOutlet} from "@angular/router";

@Component({
  selector: 'app-main',
  standalone: true,
  imports: [
    RouterOutlet,
  ],
  templateUrl: './main.component.html',
  styleUrl: './main.component.css'
})
export class MainComponent {
  constructor(private sharedService: SharedService) {}
}
