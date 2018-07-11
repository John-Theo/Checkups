import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NzMenueComponent } from './nz-menue.component';

describe('NzMenueComponent', () => {
  let component: NzMenueComponent;
  let fixture: ComponentFixture<NzMenueComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NzMenueComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NzMenueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
