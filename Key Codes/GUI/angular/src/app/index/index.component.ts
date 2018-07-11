import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {NzMessageService} from "ng-zorro-antd";

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.css']
})
export class IndexComponent implements OnInit {

  constructor(private router: Router, private message: NzMessageService) {
  }

  toUser() {this.router.navigate(['/user']);}

  classes = [
    {
      title: "体检分析",
      icon: "anticon-bar-chart",
      desc: "拍照上传或录入体检单以获得结果！",
      sub_cls: [
        {name: "血常规", icon: "blood", desc: "血液常规检查(血常规)是临床上最基础的化验检查之一，检验的是血液的细胞部分。它包括红细胞、白细胞、血红蛋白及血小板数量等。"},
        {name: "肝功能", icon: "liver", desc: "肝功能检查的目的在于探测肝脏有无疾病、肝脏损害程度以及查明肝病原因、判断预后和鉴别发生黄疸的病因等。"},
        {name: "尿常规", icon: "urine", desc: "尿常规是医学检验“三大常规”项目之一，不少肾脏病变早期就可以出现蛋白尿或者尿沉渣中有形成分。对于某些全身性病变以及身体其他脏器影响尿液改变的疾病如糖尿病、血液病、肝胆疾患、流行性出血热等的诊断，也有很重要的参考价值。"},
        {name: "骨密度", icon: "bone", desc: "亚洲人骨质疏松自我筛查工具（OSTA）可用于发现骨质疏松的高风险人群。"}
      ]
    },
    {
      title: "基本信息",
      icon: "anticon-user-add",
      desc: "基于个人基本数据的分析会更准确哦！",
      sub_cls: [
        {name: "身高", icon: "tall", desc: "身高和指标也有关系哦！"},
        {name: "体重", icon: "weight", desc: "体重和指标也有关系哦！"},
        {name: "性别", icon: "gender", desc: "性别和指标也有关系哦！"},
        {name: "年龄", icon: "age", desc: "年龄和指标也有关系哦！"}
      ]
    }
  ];

  createMessage(type: string): void {
    this.message.create(type, `This is a message of ${type}`);
  }

  ngOnInit() {
  }

}
