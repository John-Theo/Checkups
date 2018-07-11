import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PageIndexerComponent } from './page-indexer.component';

describe('PageIndexerComponent', () => {
  let component: PageIndexerComponent;
  let fixture: ComponentFixture<PageIndexerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PageIndexerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PageIndexerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
