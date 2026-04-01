import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { throttle } from 'lodash';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('Phone-Frontend');
  private http = inject(HttpClient);
  keys: string[] = ['W', 'A', 'S', 'D'];
  url: string = 'http://192.168.0.100:5000/';
  slidervalue = 0;
  isFullscreen = false;
  switch = false;
  private holdInterval: any = null;

  constructor() {
    console.log('constructor');
  }

  ngOnInit(): void {
    console.log('ngOnInit');
  }

  sendToBackend(click: string = 'lb') {
    this.http.post(`${this.url}click`, { click }).subscribe({
      next: (response) => console.log('Response from backend:', response),
      error: (err) => console.error('Error sending request to backend:', err),
    });
  }

  sendRequest(url: string, body: any) {
    this.http.post(`${this.url}${url}`, body).subscribe({
      next: () => console.log('success'),
      error: (err) => console.error('error', err),
    });
  }

  sendKey(key: string) {
    console.log('sending key', key);
    this.sendRequest('key', { key });
  }

  keyHold(key: string) {
    console.log('holding key', key);
    if (this.holdInterval) {
      clearInterval(this.holdInterval);
    }
    this.sendRequest('key-hold', { key });
  }

  keyRelease(key: string) {
    console.log('releasing key', key);
    if (this.holdInterval) {
      clearInterval(this.holdInterval);
      this.holdInterval = null;
    }
    this.sendRequest('key-release', { key });
  }

  moveMouseThrottled = throttle((x: number) => {
    console.log('moving mouse', x);
    this.sendRequest('move', { x });
  }, 100);

  moveMouse(x: string) {
    this.slidervalue = parseInt(x);
    this.moveMouseThrottled(this.slidervalue);
  }

  fullscreen(element: HTMLElement) {
    console.log('fullscreen init');

    if (!document.fullscreenElement) {
      console.log('requesting fullscreen');
      element.requestFullscreen();
      this.isFullscreen = true;
    } else {
      console.log('exiting fullscreen');
      document.exitFullscreen();
      this.isFullscreen = false;
    }
  }

  setVariant() {
    this.switch = !this.switch;
  }
}
