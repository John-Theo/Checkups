import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OuterWebComponent } from './outer-web.component';

describe('OuterWebComponent', () => {
  let component: OuterWebComponent;
  let fixture: ComponentFixture<OuterWebComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OuterWebComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OuterWebComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
