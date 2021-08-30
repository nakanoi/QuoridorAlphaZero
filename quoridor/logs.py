import os


class Log:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.loss_total = os.path.join('logs', 'loss_total.log')
        self.loss_policy = os.path.join('logs', 'loss_policy.log')
        self.loss_value = os.path.join('logs', 'loss_value.log')
        self.match_result = os.path.join('logs', 'match.log')

    def log_loss(self, hist, epoch):
        with open(self.loss_total, 'a') as f:
            for i, l in enumerate(hist.history['loss']):
                f.write('{}-{} {}\n'.format(epoch, i + 1, l))

        with open(self.loss_policy, 'a') as f:
            for i, l in enumerate(hist.history['Policy_Output_loss']):
                f.write('{}-{} {}\n'.format(epoch, i + 1, l))

        with open(self.loss_value, 'a') as f:
            for i, l in enumerate(hist.history['Value_Output_loss']):
                f.write('{}-{} {}\n'.format(epoch, i + 1, l))

    def log_result(self, results, epochs):
        with open(self.match_result, 'a') as f:
            for i, r in enumerate(results):
                f.write('{}-{} : {}\n'.format(epochs, i + 1, r))
