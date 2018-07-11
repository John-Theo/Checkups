import {Component, OnInit} from '@angular/core';
import { ActivatedRoute } from "@angular/router";

@Component({
  selector: 'app-outer-web',
  template: `    
    <app-iframe url="{{routeInfo.snapshot.params['url']}}"></app-iframe>
  `,
  styleUrls: ['./outer-web.component.css']
})

export class OuterWebComponent implements OnInit {

  constructor(public routeInfo: ActivatedRoute) { }

  ngOnInit() {
    console.log(this.routeInfo.snapshot.params['url'])
  }

}
