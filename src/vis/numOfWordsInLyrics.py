
from libinit import reader_, preper_
from matplotlib import pyplot as plt

songs = reader_.readSongs()

ly1 = songs["2011"][0]["lyrics"]
distinctWortCount, totalWordCount, words = preper_.getDistinctWords(ly1)

print(distinctWortCount)
print(totalWordCount)
print(words)



# --------------------------------------------- #
# # words
# plt.plot([0,1,2,3,4]) #, label='y = x')
# plt.title('Average number of distinct words in the lyrics')
# plt.ylabel('words')
# # years
# plt.yticks([1,2,3,4])
# plt.legend(loc = 'best')
# plt.show()
