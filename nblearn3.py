import sys
import re
import json

with open('C:/Users/Rakesh/Documents/coding-2-data-corpus/train-labeled.txt', 'r', encoding="utf-8") as f:
    content = f.read().lower()
#content = re.sub("[\[\]!\"#$%&'()*+,\-./:;<=>?@\\_\^`{|}~]",' ',content)
#content = re.sub('[ \t]+',' ',content)

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

num_lines = 0
tokens_count = {}
tokenized_data = []

num_true = 0
num_fake = 0
true_tokens_count = {}
fake_tokens_count = {}
true_tokens_prob = {}
fake_tokens_prob = {}

num_pos = 0
num_neg = 0
pos_tokens_count = {}
neg_tokens_count = {}
pos_tokens_prob = {}
neg_tokens_prob = {}
    
for line in content.splitlines():
    temp = []
    num_lines += 1 #total number of reviews
    if line.split(' ')[1] == "true":
        num_true += 1 #number of true reviews
    elif line.split(' ')[1] == "fake":
        num_fake += 1 #number of fake reviews
    if line.split(' ')[2] == "pos":
        num_pos += 1
    elif line.split(' ')[2] == "neg":
        num_neg += 1
    for word in line.split():
        word = re.sub("^[\[\]!\"#$%&'()*+,\-./:;<=>?@\\_\^`{|}~]+", ' ', str(word))
        word = re.sub("[\[\]!\"#$%&'()*+,\-./:;<=>?@\\_\^`{|}~]+$", ' ', str(word))
        word = re.sub('[ \t]+','',word)
        temp.append(word)
    tokenized_data.append(temp)

#compute class probabilities
true_class_prob = num_true/num_lines 
fake_class_prob = num_fake/num_lines
pos_class_prob = num_pos/num_lines
neg_class_prob = num_neg/num_lines

#remove stopword tokens
cleaned_data = []
for m in tokenized_data:
    stop_m = [i for i in m if str(i).lower() not in stop_words]
    cleaned_data.append(stop_m)
    
#find the count of each token in all true and fake, pos and neg reviews
for review in cleaned_data:
    for token in review[3:]:
        if token in tokens_count:
            tokens_count[token] += 1
        else:
            tokens_count[token] = 1
        if review[1] == "true":
            if token in true_tokens_count:
                true_tokens_count[token] += 1
            else:
                true_tokens_count[token] = 1
        elif review[1] == "fake":
            if token in fake_tokens_count:
                fake_tokens_count[token] += 1
            else:
                fake_tokens_count[token] = 1
        if review[2] == "pos":
            if token in pos_tokens_count:
                pos_tokens_count[token] += 1
            else:
                pos_tokens_count[token] = 1
        elif review[2] == "neg":
            if token in neg_tokens_count:
                neg_tokens_count[token] += 1
            else:
                neg_tokens_count[token] = 1 

true_tokens_denom = sum(true_tokens_count.values())+(len(tokens_count)-len(true_tokens_count))
fake_tokens_denom = sum(fake_tokens_count.values())+(len(tokens_count)-len(fake_tokens_count))
pos_tokens_denom = sum(pos_tokens_count.values())+(len(tokens_count)-len(pos_tokens_count))
neg_tokens_denom = sum(neg_tokens_count.values())+(len(tokens_count)-len(neg_tokens_count))

for key in tokens_count:
    if key in true_tokens_count:
        true_tokens_prob[key] = (true_tokens_count[key]+1)/true_tokens_denom
    else:
        true_tokens_prob[key] = 1/true_tokens_denom
    if key in fake_tokens_count:
        fake_tokens_prob[key] = (fake_tokens_count[key]+1)/fake_tokens_denom
    else:
        fake_tokens_prob[key] = 1/fake_tokens_denom
    if key in pos_tokens_count:
        pos_tokens_prob[key] = (pos_tokens_count[key]+1)/pos_tokens_denom
    else:
        pos_tokens_prob[key] = 1/pos_tokens_denom
    if key in neg_tokens_count:
        neg_tokens_prob[key] = (neg_tokens_count[key]+1)/neg_tokens_denom
    else:
        neg_tokens_prob[key] = 1/neg_tokens_denom
print(true_tokens_count)        
store_data = dict()
with open('nbmodel.txt', 'w') as outfile:
    store_data['true_class_prob'] = true_class_prob
    store_data['fake_class_prob'] = fake_class_prob
    store_data['pos_class_prob'] = pos_class_prob
    store_data['neg_class_prob'] = neg_class_prob
    store_data['true_tokens_prob'] = dict()
    store_data['true_tokens_prob'] = true_tokens_prob
    store_data['fake_tokens_prob'] = dict()
    store_data['fake_tokens_prob'] = fake_tokens_prob
    store_data['pos_tokens_prob'] = dict()
    store_data['pos_tokens_prob'] = pos_tokens_prob
    store_data['neg_tokens_prob'] = dict()
    store_data['neg_tokens_prob'] = neg_tokens_prob
    outfile.write(json.dumps(store_data))