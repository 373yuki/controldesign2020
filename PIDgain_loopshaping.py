### 参考：https://qiita.com/hanon/items/d5afd8ea3f1e2e7b0d32
from control.matlab import *
import numpy as np
from ipywidgets import interact
from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure, output_file
from bokeh.layouts import row, column

output_notebook() # jupyterNotebookに出力

### 描画
## 初期データ

#制御対象
#K  = 0.9
#z  = 0.5
#wn = 3
#G2 = tf( [K*wn**2], [1, 2*z*wn, wn**2] )
g  = 9.81                # 重力加速度[m/s^2]
l  = 0.2                 # アームの長さ[m]
m  = 0.5                 # アームの質量[kg]
c  = 1.5e-2              # 粘性摩擦係数[kg*m^2/s]
J  = 1.0e-2              # 慣性モーメント[kg*m^2]
ref = 30
G2 = tf( [0,1], [J, c, m*g*l] )
G = G2
#P制御（kp=1）
C = tf([0.1],[0, 1]) 
Gyr = feedback(G*C, 1)
y,t = step(Gyr, np.arange(0, 5, 0.01))

gain, _, w = bode(Gyr, logspace(-2, 2), Plot=False)

## figureを宣言
p1 = figure(title = "Step Response",
          plot_height = 250,
          plot_width = 350,
          y_range=(0,2),
          x_axis_label='t [s]',
          y_axis_label='y')

## figureを宣言
p2 = figure(title = "Phase Diagram",
          plot_height = 200,
          plot_width = 400,
          x_axis_type = 'log',
          y_range = (-270, 90),
          x_axis_label='w [rad/s]',
          y_axis_label='Phase [deg]')

## figureを宣言
p3 = figure(title = "Gain Diagram",
          plot_height = 200,
          plot_width = 400,
          x_axis_type = 'log',
          y_range = (-80, 60),
          x_axis_label='w [rad/s]',
          y_axis_label='Gain [dB]')

## rendererを追加
p1.line(t, 1*(t>0))
r1 = p1.line(t, y, line_width = 3, color='red')
gain, phase, w = bode(G*C, logspace(-2,2), Plot=False)
p2.line(w, -180)
r3 = p3.line(w, 20*np.log10(gain), line_width = 3)
r2 = p2.line(w, 180/np.pi*phase, line_width = 3)



## interactorを定義
def update(kp=0.1, kd=0, ki=0):
    #G = G2 * tf([1],[T3, 1])
    C = tf([kd, kp, ki], [1, 0])  
    Gyr = feedback(G*C, 1)
    yout,_ = step(Gyr, np.arange(0, 5, 0.01))
    r1.data_source.data['y'] = yout
    pole = Gyr.pole();
    gain, phase, _ = bode(G*C, logspace(-2,2), Plot=False)
    r3.data_source.data['y'] = 20*np.log10(gain)
    r2.data_source.data['y'] = 180/np.pi*phase
    push_notebook()

## 描画
p0 = column(p3,p2)
p = row(p0, p1)
show(p, notebook_handle=True) # notebook_handleをTrueにすると後から図を制御出来る

## interactorの実行
interact(update, kp = (0.1, 20, 0.1), kd = (0, 5, 0.05), ki = (0, 10, 0.1) )