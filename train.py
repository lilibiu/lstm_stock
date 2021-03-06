# -*- utf-8 -*-
import tensorflow as tf
import os
from preprogress import generate_data
from model import multi_bilstm_model

tf.app.flags.DEFINE_integer("batch_size", 64, "batch size")
tf.app.flags.DEFINE_integer("time_step", 30, "input size")
tf.app.flags.DEFINE_integer("hidden_size", 32, "hidden layer size")
tf.app.flags.DEFINE_integer("layer_num", 2, "hidden layer num")

tf.app.flags.DEFINE_integer("start_learning_rate", 0.1, "start learning rate")
tf.app.flags.DEFINE_integer("training_step", 10000, "training steps")

tf.app.flags.DEFINE_string("model_path", os.path.abspath("./model"), "save model to this path")
tf.app.flags.DEFINE_string("data_path", os.path.abspath("./data/SH000001_2_train.csv"), "model path")

FLAGS = tf.app.flags.FLAGS


def main(_):
    if not os.path.exists(FLAGS.model_path):
        os.makedirs(FLAGS.model_path)

    train_x, train_y, _, _ = generate_data(FLAGS.data_path, FLAGS.time_step)
    num = (len(train_x) // FLAGS.batch_size) * FLAGS.batch_size
    train_x = train_x[:num]
    train_y = train_y[:num]
    # print(np.shape(train_x), np.shape(train_y))

    ds = tf.contrib.data.Dataset.from_tensor_slices((train_x, train_y))
    ds = ds.shuffle(1000).batch(FLAGS.batch_size).repeat()
    x, y = ds.make_one_shot_iterator().get_next()
    # print(x.get_shape(), y.get_shape())
    # exit(0)

    with tf.variable_scope("model"):
        prediction, loss, train_op = multi_bilstm_model(x, y, is_training=True, batch_size=FLAGS.batch_size,
                                                        hidden_size=FLAGS.hidden_size, layer_num=FLAGS.layer_num,
                                                        start_lr=FLAGS.start_learning_rate)
    saver = tf.train.Saver()
    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_op)
        for step in range(FLAGS.training_step):
            _, l = sess.run([train_op, loss])
            if step % 100 == 0:
                print("train step: %d, loss: %s" % (step, ("%.6f" % l)))
                saver.save(sess, os.path.join(FLAGS.model_path, "stock"), global_step=step)


if __name__ == "__main__":
    tf.app.run()
