import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class CoreService {
  private apiUrl = 'http://your-odoo-server/api/client'; // Replace with your actual API URL

  constructor(private http: HttpClient) {}

  createClient(clientData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/create`, clientData);
  }

  updateClient(clientId: number, clientData: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/update/${clientId}`, clientData);
  }

  deleteClient(clientId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete/${clientId}`);
  }

  getClientById(clientId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/get/${clientId}`);
  }

  getAllClients(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/get-all`);
  }

  login(email: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, { email, password });
  }

  logout(): Observable<any> {
    return this.http.post(`${this.apiUrl}/logout`, {});
  }
}
