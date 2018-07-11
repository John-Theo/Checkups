import {Component, OnInit} from '@angular/core';
import { Observable } from 'rxjs/Rx';
import {Router} from "@angular/router";
import {MalihuScrollbarService} from "ngx-malihu-scrollbar";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls  : ['./app.component.css']
})
export class AppComponent implements OnInit{

  private content: string = 'Content Hi!';
  private app_height_delta: number = 186;
  private window_height: string = (window.innerHeight-this.app_height_delta).toString()+"px";

  constructor(private router: Router, private mScrollbarService: MalihuScrollbarService){}

  toUpload(){ this.router.navigate(['/upload']); }
  toIndex(){ this.router.navigate(['/index']); }
  toCheck(){ this.router.navigate(['/check']); }
  toReport(){ this.router.navigate(['/report']); }
  toAnalyze(){ this.router.navigate(['/analyze']); }
  toUrl(url: string){ this.router.navigate(['/outer_web', url]); }

  ngOnInit() {
    let that = this;

    Observable.fromEvent(window,'resize').subscribe(() => {
      // console.log(window.innerHeight);
      that.window_height = (window.innerHeight-that.app_height_delta).toString()+'px';
      that.content = that.window_height;
    });
  }

  public scrollbarOptions = {
    axis: 'y',
    theme: 'dark-3',
  };

  openMap = {
    sub1: true,
    sub2: false,
    sub3: false
  };

  openHandler(value: string): void {
    for (const key in this.openMap) {
      if (key !== value) {
        this.openMap[ key ] = false;
      }
    }
  }

}
