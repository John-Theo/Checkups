import {Component, Input, OnChanges, OnInit} from '@angular/core';
import {DomSanitizer} from "@angular/platform-browser";

@Component({
  selector: 'app-iframe',
  template: `
    <div>
    <iframe nz-col class="report-iframe" width="{{page_configure[url][0]}}px" height="{{page_configure[url][1]}}px"
            seamless frameBorder="0" [src]="safe_url"></iframe>
    </div>
  `,
  styleUrls: ['./iframe.component.css']
})
export class IframeComponent implements OnInit, OnChanges {

  constructor(private sanitizer: DomSanitizer) { }

  @Input()
  url: string;

  safe_url: object;
  page_configure = {
    "wegene": [1280, 4777],
    "23mofang": [1280, 6377]
  };

  ngOnChanges(){
    this.safe_url = this.sanitizer.bypassSecurityTrustResourceUrl("https://www."+this.url+".com");
  }

  ngOnInit() {
    this.safe_url = this.sanitizer.bypassSecurityTrustResourceUrl("https://www."+this.url+".com");
  }

}
