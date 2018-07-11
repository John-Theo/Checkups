import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-info-check',
  templateUrl: './info-check.component.html',
  styleUrls: ['./info-check.component.css'],
})
export class InfoCheckComponent implements OnInit {

  private column = 2;
  public scrollbarOptions = { axis: 'yx', theme: 'minimal-dark' };

  columns = [];

  user_info = [
    {term: '身高', unit: 'cm', value: 176},
    {term: '体重', unit: 'kg', value: 70},
    {term: '年龄', unit: '周岁', value: 21},
  ];

  test_info = [
    {id: 'WBC', term: '白细胞计数', unit: ['10^9/L', 'test'], value: 1},
    {id: 'RBC', term: '红细胞计数', unit: ['10^12/L'], value: null},
    {id: 'HB', term: '血红蛋白浓度', unit: ['g/L'], value: 3},
    {id: 'HCT', term: '红细胞压积', unit: ['%'], value: null},
    {id: 'MCV', term: '平均红细胞体积', unit: ['fL'], value: 5},
    {id: 'MCH', term: '平均红细胞血红蛋白含量', unit: ['pg'], value: null},
    {id: 'MCHC', term: '平均红细胞血红蛋白浓度', unit: ['g/L'], value: null},
    {id: 'PLT', term: '血小板计数', unit: ['10^9/L'], value: null},
    {id: 'LY%', term: '淋巴细胞比值', unit: ['%'], value: null},
    {id: 'MONO%', term: '单核细胞比例', unit: ['%'], value: null},
    {id: 'NEUT%', term: '中性粒细胞比例', unit: ['%'], value: null},
    {id: 'LY', term: '淋巴细胞计数', unit: ['10^9/L'], value: null},
    {id: 'MONO', term: '单核细胞计数', unit: ['10^9/L'], value: null},
    {id: 'NEUT', term: '中性粒细胞计数', unit: ['10^9/L'], value: null},
    {id: 'RDW', term: '红细胞分布宽度', unit: ['%'], value: null},
    {id: 'PDW', term: '血小板体积分布宽度', unit: ['%'], value: 16},
    {id: 'MPV', term: '血小板体积分布宽度', unit: ['fL'], value: null},
    {id: 'P-LCR', term: '大血小板比例', unit: ['%'], value: 18},
  ];

  test_group = [];
  odd_flag = 0;

  constructor() {}

  ngOnInit(): void {

    for (let i=0; i<this.test_info.length; i++){
      this.test_info[i].value = Math.ceil(Math.random()*50);
    }

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
