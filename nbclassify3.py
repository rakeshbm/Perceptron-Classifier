# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 17:54:21 2018

@author: Rakesh
"""

import json
import sys
import re
from math import log

with open('nbmodel.txt', 'r') as f:
    data = json.loads(f.read())
  
true_class_prob = data['true_class_prob']
fake_class_prob = data['fake_class_prob']
pos_class_prob = data['pos_class_prob']
neg_class_prob = data['neg_class_prob']
true_tokens_prob = data['true_tokens_prob']
fake_tokens_prob = data['fake_tokens_prob']
pos_tokens_prob = data['pos_tokens_prob']
neg_tokens_prob = data['neg_tokens_prob']

s = """a
about
above
across
after
again
against
all
almost
alone
along
already
also
although
always
among
an
and
another
any
anybody
anyone
anything
anywhere
are
area
areas
around
as
ask
asked
asking
asks
at
away
b
back
backed
backing
backs
be
became
because
become
becomes
been
before
began
behind
being
beings
best
better
between
big
both
but
by
c
came
can
cannot
case
cases
certain
certainly
clear
clearly
come
could
d
did
differ
different
differently
do
does
done
down
downed
downing
downs
during
e
each
early
either
end
ended
ending
ends
enough
even
evenly
ever
every
everybody
everyone
everything
everywhere
f
face
faces
fact
facts
far
felt
few
find
finds
first
for
four
from
full
fully
further
furthered
furthering
furthers
g
gave
general
generally
get
gets
give
given
gives
go
going
good
goods
got
great
greater
greatest
group
grouped
grouping
groups
h
had
has
have
having
he
her
here
herself
high
higher
highest
him
himself
his
how
however
i
if
important
in
interest
interested
interesting
interests
into
is
it
its
itself
j
just
k
keep
keeps
kind
knew
know
known
knows
l
large
largely
last
later
latest
least
less
let
lets
like
likely
long
longer
longest
m
made
make
making
man
many
may
me
member
members
men
might
more
most
mostly
mr
mrs
much
must
my
myself
n
necessary
need
needed
needing
needs
never
new
newer
newest
next
no
nobody
non
noone
not
nothing
now
nowhere
number
numbers
o
of
off
often
old
older
oldest
on
once
one
only
open
opened
opening
opens
or
order
ordered
ordering
orders
other
others
our
out
over
p
part
parted
parting
parts
per
perhaps
place
places
point
pointed
pointing
points
possible
present
presented
presenting
presents
problem
problems
put
puts
q
quite
r
rather
really
right
room
rooms
s
said
same
saw
say
says
second
seconds
see
seem
seemed
seeming
seems
sees
several
shall
she
should
show
showed
showing
shows
side
sides
since
small
smaller
smallest
so
some
somebody
someone
something
somewhere
state
states
still
such
sure
t
take
taken
than
that
the
their
them
then
there
therefore
these
they
thing
things
think
thinks
this
those
though
thought
thoughts
three
through
thus
to
today
together
too
took
toward
turn
turned
turning
turns
two
u
under
until
up
upon
us
use
used
uses
v
very
w
want
wanted
wanting
wants
was
way
ways
we
well
wells
went
were
what
when
where
whether
which
while
who
whole
whose
why
will
with
within
without
work
worked
working
works
would
x
y
year
years
yet
you
young
younger
youngest
your
yours
z"""

stop_words = []
stop_words = s.split()

with open('C:/Users/Rakesh/Documents/coding-2-data-corpus/dev-text.txt', 'r', encoding="utf-8") as f:
	content = f.read().lower()
  
tokenized_data = []
for line in content.splitlines():
    temp = []
    for word in line.split():
        word = re.sub("^[\[\]!\"#$%&'()*+,\-./:;<=>?@\\_\^`{|}~]+", ' ', str(word))
        word = re.sub("[\[\]!\"#$%&'()*+,\-./:;<=>?@\\_\^`{|}~]+$", ' ', str(word))
        word = re.sub('[ \t]+','',word)
        temp.append(word)
    tokenized_data.append(temp)

cleaned_data = []
for m in tokenized_data:
    stop_m = [i for i in m if str(i).lower() not in stop_words]
    cleaned_data.append(stop_m)
   
true_tokens_denom = sum(true_tokens_count.values())+(len(tokens_count)-len(true_tokens_count))
fake_tokens_denom = sum(fake_tokens_count.values())+(len(tokens_count)-len(fake_tokens_count))
pos_tokens_denom = sum(pos_tokens_count.values())+(len(tokens_count)-len(pos_tokens_count))
neg_tokens_denom = sum(neg_tokens_count.values())+(len(tokens_count)-len(neg_tokens_count))
   
file = open("nboutput.txt", "w", encoding="utf-8")

for review in cleaned_data:
    true = log(true_class_prob)
    fake = log(fake_class_prob)
    pos = log(pos_class_prob)
    neg = log(neg_class_prob)
    for token in review[1:]:
        if token in true_tokens_prob:
            true += log(true_tokens_prob[token])
        else:
            true += log(1/true_tokens_denom)
        if token in fake_tokens_prob:
            fake += log(fake_tokens_prob[token])
        else:
            fake += log(1/fake_tokens_denom)
        if token in pos_tokens_prob:
            pos += log(pos_tokens_prob[token])
        else:
            pos += log(1/pos_tokens_denom)
        if token in neg_tokens_prob:
            neg += log(neg_tokens_prob[token])
        else:
            neg += log(1/neg_tokens_denom)
    file.write(review[0])
    if true>fake:
        file.write(" True")
    else:
        file.write(" Fake")
    if pos>neg:
        file.write(" Pos")
    else:
        file.write(" Neg")
    file.write("\n")

file.close()