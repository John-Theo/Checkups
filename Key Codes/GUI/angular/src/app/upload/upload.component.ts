import { Component } from '@angular/core';
import { NzMessageService, UploadFile } from 'ng-zorro-antd';

@Component({
  selector: 'app-upload',
  template: `
  <nz-upload
    nzType="drag"
    nzListType="picture-card"
    nzLimit="1"
    nzAction="https://jsonplaceholder.typicode.com/posts/"
    (nzChange)="handleChange($event)">
    <p class="ant-upload-drag-icon">
      <i class="anticon anticon-inbox"></i>
    </p>
    <p class="ant-upload-text">点击或拖拽文件</p>
    <p class="ant-upload-hint">一次只能上传一张图片</p>
  </nz-upload>
  `,
  styles: [
    `
  :host ::ng-deep nz-upload { display: block; }
  :host ::ng-deep .ant-upload.ant-upload-drag { height: 400px; }
  `
  ]
})
export class UploadComponent {
  constructor(private msg: NzMessageService) {}
  handleChange({ file, fileList }): void {
    const status = file.status;
    if (status !== 'uploading') {
      console.log(file, fileList);
    }
    if (status === 'done') {
      this.msg.success(`${file.name} file uploaded successfully.`);
    } else if (status === 'error') {
      this.msg.error(`${file.name} file upload failed.`);
    }
  }
}
