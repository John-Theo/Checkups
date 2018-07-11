import { NgModule } from "@angular/core";
import { Routes, RouterModule} from "@angular/router";
import { IndexComponent } from "./index/index.component";
import { ChooseComponent } from "./choose/choose.component";
import {InfoCheckComponent} from "./info-check/info-check.component";
import {ReportComponent} from "./report/report.component";
import {ExportComponent} from "./export/export.component";
import {Code404Component} from "./code404/code404.component";
import {DataInputComponent} from "./data-input/data-input.component";
import {OuterWebComponent} from "./outer-web/outer-web.component";
import {AnalyzeComponent} from "./analyze/analyze.component";

const routes: Routes = [
  { path: '', component: IndexComponent },
  { path: 'index', component: IndexComponent },
  { path: 'upload', component: DataInputComponent },
  { path: 'choose', component: ChooseComponent },
  { path: 'check', component: InfoCheckComponent },
  { path: 'report', component: ReportComponent },
  { path: 'export', component: ExportComponent },
  { path: 'analyze', component: AnalyzeComponent },
  { path: 'outer_web/:url', component: OuterWebComponent },
  { path: '**', component: Code404Component },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: []
})

export class AppRoutingModule {}
