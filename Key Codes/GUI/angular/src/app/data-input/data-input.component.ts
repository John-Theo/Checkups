import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-data-input',
  templateUrl: './data-input.component.html',
  styles: [
      `
      [nz-form]:not(.ant-form-inline):not(.ant-form-vertical) {
        max-width: 600px;
      }
    `
  ]
})
export class DataInputComponent implements OnInit {

  panels = [
    {
      active: true,
      name: '手动输入',
      disabled: false
    }
  ];

  private column = 2;
  columns = [];

  test_info = [
    {id: 'WBC', term: '白细胞计数', unit: ['10^9/L', 'test']},
    {id: 'RBC', term: '红细胞计数', unit: ['10^12/L']},
    {id: 'HB', term: '血红蛋白浓度', unit: ['g/L']},
    {id: 'HCT', term: '红细胞压积', unit: ['%']},
    {id: 'MCV', term: '平均红细胞体积', unit: ['fL']},
    {id: 'MCH', term: '平均红细胞血红蛋白含量', unit: ['pg']},
    {id: 'MCHC', term: '平均红细胞血红蛋白浓度', unit: ['g/L']},
    {id: 'PLT', term: '血小板计数', unit: ['10^9/L']},
    {id: 'LY%', term: '淋巴细胞比值', unit: ['%']},
    {id: 'MONO%', term: '单核细胞比例', unit: ['%']},
    {id: 'NEUT%', term: '中性粒细胞比例', unit: ['%']},
    {id: 'LY', term: '淋巴细胞计数', unit: ['10^9/L']},
    {id: 'MONO', term: '单核细胞计数', unit: ['10^9/L']},
    {id: 'NEUT', term: '中性粒细胞计数', unit: ['10^9/L']},
    {id: 'RDW', term: '红细胞分布宽度', unit: ['%']},
    {id: 'PDW', term: '血小板体积分布宽度', unit: ['%']},
    {id: 'MPV', term: '血小板体积分布宽度', unit: ['fL']},
    {id: 'P-LCR', term: '大血小板比例', unit: ['%']},
  ];

  test_group = [];
  odd_flag = 0;

  constructor() {}

  ngOnInit(): void {
    if (this.test_info.length % this.column != 0) {
      this.odd_flag = 1;
    }
    let column_len = Math.floor(this.test_info.length / this.column) + this.odd_flag;
    for (let i = 0; i < this.column; i++) {
      let slice_start = column_len * i;
      let slice_end = slice_start + column_len;
      this.test_group.push(this.test_info.slice(slice_start, slice_end));
      this.columns.push(i)
    }

  }
}
