"""
参考莫烦python教程
本code使用TensorFlow搭建一个简单的神经网络，并且包含使用matplotlib中的可视化实验结果。
plt.ion()函数搭配remove函数实现在一张图中更新可视化结果

"""
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


def add_layer(inputs, in_size, out_size, activation_function=None):
    weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    wx_plus_b = tf.matmul(inputs, weights) + biases
    if activation_function is None:
        outputs = wx_plus_b
    else:
        outputs = activation_function(wx_plus_b)
    return outputs


x_data = np.linspace(-1, 1, 500)[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape)
y_data = np.square(x_data) - 0.5 + noise

xs = tf.placeholder(tf.float32, [None, 1])
ys = tf.placeholder(tf.float32, [None, 1])
L1 = add_layer(xs, 1, 10, activation_function=tf.nn.relu)
prediction = add_layer(L1, 10, 1, activation_function=None)

loss = tf.reduce_mean(
    tf.reduce_sum(
        tf.square(
            ys - prediction),
        reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)
init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(x_data, y_data)
plt.ion()
plt.show()


for i in range(3000):
    sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
    if i % 50 == 0:
        # print(sess.run(loss, feed_dict={xs: x_data, ys: y_data}))
        try:
            ax.lines.remove(lines[0])
        except Exception:
            pass

        prediction_v = sess.run(prediction, feed_dict={xs: x_data})
        lines = ax.plot(x_data, prediction_v, 'r-', lw=5)
        plt.pause(0.1)
