import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {ProductComponent} from "./pages/product/product.component";
import {StoreComponent} from "./pages/store/store.component";
import {LayoutComponent} from "../../shared/components/layout/layout.component";


const routes: Routes = [
  {
    path: '',
    component: LayoutComponent,
    children: [
      { path: '', component: StoreComponent },
      { path: 'pharmcay', component: StoreComponent },
      { path: 'medicine', component: ProductComponent },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PharmacyRoutingModule { }
