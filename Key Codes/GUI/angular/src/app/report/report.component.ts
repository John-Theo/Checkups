import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.css']
})
export class ReportComponent implements OnInit {

  pdfSrc: string = '../../assets/report_blood.pdf';

  constructor() { }

  ngOnInit() {
  }

}
