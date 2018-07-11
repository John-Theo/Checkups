import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { NgZorroAntdModule } from 'ng-zorro-antd';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { FooterComponent } from './footer/footer.component';
import { NzMenuComponent } from './nz-menu/nz-menu.component';
import { UploadComponent } from './upload/upload.component';
import { DataInputComponent } from './data-input/data-input.component';
import { PageIndexerComponent } from './page-indexer/page-indexer.component';
import { IndexComponent } from './index/index.component';
import { MainAppComponent } from './main-app/main-app.component';
import { AppRoutingModule } from './app-routing.module';
import { ChooseComponent } from './choose/choose.component';
import { InfoCheckComponent } from './info-check/info-check.component';
import { ReportComponent } from './report/report.component';
import { ExportComponent } from './export/export.component';
import { Code404Component } from './code404/code404.component';
import { OuterWebComponent } from './outer-web/outer-web.component';
import { IframeComponent } from './iframe/iframe.component';
import { MalihuScrollbarModule } from 'ngx-malihu-scrollbar';
import { AnalyzeComponent } from './analyze/analyze.component';

import { PdfViewerModule } from 'ng2-pdf-viewer';
import {platformBrowserDynamic} from "@angular/platform-browser-dynamic";


@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    FooterComponent,
    NzMenuComponent,
    UploadComponent,
    DataInputComponent,
    PageIndexerComponent,
    IndexComponent,
    MainAppComponent,
    ChooseComponent,
    InfoCheckComponent,
    ReportComponent,
    ExportComponent,
    Code404Component,
    OuterWebComponent,
    IframeComponent,
    AnalyzeComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    NgZorroAntdModule.forRoot(),
    MalihuScrollbarModule.forRoot(),
    PdfViewerModule,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

platformBrowserDynamic().bootstrapModule(AppModule);
