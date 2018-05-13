import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch.nn.parameter import Parameter
from torch.nn.init import xavier_normal, xavier_uniform, orthogonal


class TextEncoder(nn.Module):
    """
    Bi-LSTM encoder for textual input. Can be incorporated into multi-attention.
    The shared memory modulates the word-level attention,
    as per DAN paper, i.e. the shared memory affects how the word encodings are attended to,
    but now how they were derived from the word embeddings via recurrent encoding.
    """
    def __init__(self, in_size, hid_size, out_size, num_layers=1, dropout=0.2, bidirectional=False):


        super(TextEncoder, self).__init__()
        self.rnn = nn.LSTM(in_size, hid_size, num_layers=num_layers, dropout=droupout,
                           bidirectional=bidirectional, batch_first=True)

    def forward(self, x):
        """

        param x: tensor of shape (batch_size, seq_len, in_size)
        """
        output, final_hiddens = self.rnn(x)

        return output, final_hiddens

class TextOnlyModel(nn.Module):
    """
    Text only model. Encodes with TextEncoder and then projects final hidden state through a FC layer
    """
    def __init__(self, in_size, hid_size, out_size, num_layers=1, rnn_dropout=0.2, post_dropout=0.2, bidirectional=False, output_scale_factor=1, output_shift=0):

        super(TextOnlyModel, self).__init__()
        self.rnn_enc = TextEncoder(in_size, hid_size, out_size, num_layers=num_layers, dropout=rnn_dropout, bidirectional=bidirectional, batch_first=True)
        self.dropout = nn.Dropout(dropout)
        self.linear_last = nn.Linear(hid_size, out_size)
        self.output_scale_factor = Parameter(torch.FloatTensor([output_scale_factor]), requires_grad=False)
        self.output_shift = Parameter(torch.FloatTensor([output_shift]), requires_grad=False)

    def forward(self, x):
        """

        param x: tensor of shape (batch_size, seq_len, in_size)
        """
        _, final_hiddens = self.rnn_enc(x)

        final_h_drop = self.dropout(final_hiddens[0].squeeze())
        y = F.sigmoid(self.linear_last(final_h_drop))
        y = y*self.output_scale_factor + self.output_shift

        return y


# class TextEncoderWrapper:
#     """
#     Wrapper for TextEncoder to be used when we want an encapsulated way to access all h and c states
#     of the rnn. Pytorch's LSTM class only outputs (i) the hidden states of the *final* layer at each
#     time step t=1:seq_len, and (ii) the (h, c) states for final step t=seq_len
#     """

class TextEncoderExtContext(nn.Module):
    """
    Bi-LSTM encoder for textual input which incorporates an external memory state into the
    encoding dynamics when generating a latent summary state.
    """
    def __init__(self, in_size, hid_size, out_size, num_layers=1, dropout=0.2, bidirectional=False):


        super(TextEncoder, self).__init__()
        self.rnn = nn.LSTM(in_size, hid_size, num_layers=num_layers, droupout=droupout,
                           bidirectional=bidirectional, batch_first=True)
        self.dropout = nn.Dropout(dropout)
        self.linear_last = nn.Linear(hid_size, out_size)
        self.m2h_proj = nn.Linear(mem_size, hid_size*num_layers)
        self.m2c_proj = nn.Linear(mem_size, hid_size*num_layers)

    def forward(self, x, ext_memory=None):
        """
        param x: the input sequence of word embeddings
        type x: tensor of shape (batch_size, seq_len, in_size)
        param ext_memory: external shared memory which provides a context for the encoder
                          via an initial hidden state
        type ext_memory: tensor of shape (batch_size, mem_size)
        """
        if ext_memory:
            h_init = self.m2h_proj(ext_memory)
            c_init = self.m2c_proj(ext_memory)
            output, final_hiddens = self.rnn(x, (h_init, c_init))
            # TODO: do we need a final FC projection here (preceded by dropout)?
        else:
            output, final_hiddens = self.rnn(x)
            # TODO: do we need a final FC projection here (preceded by dropout)?

        return output, final_hiddens





