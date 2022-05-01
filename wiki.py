
def read_article_links(file_name):
    """
    :param file_name: name of the file to open
    :return: a list of pairs (tuples) every article and the article it links to
    """
    f = open(file_name, 'r')
    links_lst = []
    for line in f:
        pair_str = line.split('\t')  # split tab
        a1 = pair_str[0]
        a2 = pair_str[1].replace("\n", "")  # remove "\n" from every pair[1]
        tpl = a1, a2
        links_lst.append(tpl)
    return links_lst


class Article:
    """
    A class representing an Article Object
    Every Article has a name and neighbors (Article Objects) and a rank as well
    """

    def __init__(self, name):
        """
        Create an article object
        :param name: name of article
        """
        self.__name = name
        self.__neighbours = []  # article neighbours that this article leads to

        self.__article_page_rank = 0
        self.__in_deg = 0  # in degree (for task 4)

    def get_name(self):
        """
        :return: name of article
        """
        return self.__name

    def add_neighbor(self, neighbor):
        """
        this method adds a neighbor to this article
        :param neighbor: Other article object that is neighbor to this article
        """
        neighbor.add_in_deg()
        self.__neighbours.append(neighbor)

    def get_neighbors(self):
        """
        :return: neighbors list of this article
        """
        return self.__neighbours

    def __repr__(self):
        """
        Return a string representation of the Article.
        :return: A tuple converted to string. The tuple's content should be:
            1. Name of the article
            2. List contains the names of all its neighbours
        """
        article_name = self.__name

        neighbors_name_lst = []
        for neighbor in self.__neighbours:
            neighbors_name_lst.append(neighbor.get_name())

        tpl = article_name, neighbors_name_lst
        return str(tpl)

    def __len__(self):
        """
        :return: number of neighbors of the Article
        """
        return len(self.__neighbours)

    def __contains__(self, article):
        """
        Checks wither an article is a neighbor or not
        :param article: Article object
        :return:
            If article in neighbors list: True
            else return: Falsr
        """
        if article in self.__neighbours:
            return True
        else:
            return False

    def get_neighbors_names(self):
        """
        :return: A list of all the names of the Article's neighbors
        """
        neighbors_name_lst = []
        for neighbor in self.__neighbours:
            neighbors_name_lst.append(neighbor.get_name())
        return neighbors_name_lst

    def get_page_rank(self):
        """
        :return the current page rank of the article
        """
        return self.__article_page_rank

    def set_page_rank(self, value):
        """
        This method changes the current page rank of the article by a given
        value
        :param value: how much we want to change the value of the page rank
        of the article
        """
        self.__article_page_rank += value

    def get_in_deg(self):
        """
        :return: in degree of the article
        """
        return self.__in_deg

    def add_in_deg(self):
        """
        This method adds one degree to the article when it's called
        """
        self.__in_deg += 1


class WikiNetwork:
    """
    A Class representing the Wikipedia Network
    The Network is composed of Articles and it's Article neighbors (Article
    neighbor means that for example if A links to Article B then B is a
    neighbor of A)
    """

    def __init__(self, link_list=[]):
        """
        The constructor of object WikiNetwork
        :param link_list: A list of pairs in tuples. every pair is an
        Article and the Article it links to
        """
        self.__link_list = []
        self.__articles_dict = {}
        self.__dict_obj = {}
        self.__articles_lst = []
        self.__articles_names_lst = []
        self.__page_rank_dict = {}

        # builds the network by calling the update network function
        self.update_network(link_list)

    def update_network(self, link_list):
        """
        This method gets a list of article pairs and update the network
        :param link_list: A list of pairs in tuples. every pair is an
        Article and the Article it links to
        """
        # Note: some lists and dictionaries in this function was not
        #  required but i needed to update them for later use in the exercise
        for tpl in link_list:
            self.__link_list.append(tpl)

        for line_idx in range(len(link_list)):
            a1 = link_list[line_idx][0]  # get the name in column A
            a2 = link_list[line_idx][1]  # get the name in column B

            # If articles not already in network add them
            if a1 not in self.__dict_obj:
                self.__dict_obj[a1] = Article(a1)

            if a2 not in self.__dict_obj:
                self.__dict_obj[a2] = Article(a2)

        for pair in link_list:
            article = (self.__dict_obj[pair[0]])
            article_neighbor = (self.__dict_obj[pair[1]])
            # add neighbor to the article only if not already exists
            if article_neighbor not in article.get_neighbors():
                article.add_neighbor(article_neighbor)

        for article in self.__dict_obj:
            article_obj = self.__dict_obj[article]
            self.__articles_dict[article_obj] = article_obj.get_neighbors()
            self.__articles_lst.append(article_obj)

    def get_articles(self):
        """
        :return: list of all articles (Objects) in the network
        """
        return self.__articles_lst

    def get_titles(self):
        """
        :return: A list of all articles names in the network
        """
        for key in self.__dict_obj:
            self.__articles_names_lst.append(key)
        return self.__articles_names_lst

    def __contains__(self, article_name):
        """
        This method checks if an article is in the network by it's name
        :param article_name: the name of the article
        :return: if article name exists in the network = True
        """
        if article_name in self.get_titles():
            return True
        else:
            return False

    def __len__(self):
        """
        :return: the number of articles in the network
        """
        return len(self.__articles_lst)

    def __repr__(self):
        """
        Return a string representation of WikiNetwork.
        :return: a dictionary represented as string that it's keys are the
        names of the articles and it's values are articles (objects)
        """
        return str(self.__dict_obj)

    def __getitem__(self, article_name):
        """
        :param article_name: name of the article
        :return:
            1. if name of the article exists in the network return the
               object that matches this name
            2. if name of the article not found in network raise KeyError
        """
        return self.__dict_obj[article_name]

    def update_page_rank(self, d):
        """
        This is a function helper for page_rank
        This method calculates and changes the ranks of the articles everytime
        it was called
        """
        page_rank_older_dict = {}  # ranks until the previous iter stored here
        EXTRA = 1 - d  # (0.1)

        for article in self.__page_rank_dict:
            # holds the ranks until the previous iter
            page_rank_older_dict[article] = self.__page_rank_dict[article]

        for article in self.__articles_lst:
            # the rank until the previous iteration
            rank = page_rank_older_dict[article]

            article_neighbors = article.get_neighbors()  # list of neighbors
            val = d*rank
            # removing the current rank of the article
            article.set_page_rank((-1)*rank)

            if len(article_neighbors) != 0:  # article has neighbors
                for neighbor in article_neighbors:  # for every neighbor
                    # give every neighbor: d*(previous rank) / num of neighbors
                    neighbor.set_page_rank(round(val / len(
                        article_neighbors), 3))
                for any_article in self.__articles_lst:  # for all articles
                    # give all the articles (1-d) / num of articles in network
                    any_article.set_page_rank(EXTRA / len(self.__articles_lst))

        for article in self.__articles_lst:
            # add the article to the dictionary as a key and it's value
            #  as it's page rank
            self.__page_rank_dict[article] = article.get_page_rank()

    def page_rank(self, iters, d=0.9):
        """
        This method ranks the articles in network by a giving formula and
        number of iterations
        :param iters: how many iterations
        :return: a sorted list of articles by their page rank first then by
        name if more than an article has the same page rank value
        """
        self.__page_rank_dict = {}
        for article in self.__articles_lst:
            article.set_page_rank(1)  # give every article rank value of (1)
            self.__page_rank_dict[article] = article.get_page_rank()

        for iteration in range(iters):  # iters = number of iterations
            # use the function helper to calculate and change the ranks
            #  of the  article every iteration
            self.update_page_rank(d)  # (d=0.9)

        # SORT #####
        dict_names = {}
        for article in self.__articles_lst:
            dict_names[article.get_name()] = article.get_page_rank()

        sorted_list_names = []
        # The following line sorts the dictionary to a list by
        #  page rank (value) then by name if same values (by key)
        for key in sorted(dict_names.items(), key=lambda x: (-x[1], x[0])):
            sorted_list_names.append(key[0])

        return sorted_list_names

    def jaccard_index(self, article_name):
        """
        This method calculates the jaccard index
        :param article_name: the name of the article
        :return: a sorted list by the index jaccard then by alphabet if same
        value.
        """
        # Index Jaccard = The intersection of A and B / Union of A and B
        #  (A and B are sets of articles)
        if self.__contains__(article_name):
            article_obj = self.__dict_obj[article_name]  # get the object article
            article1_neighbors = article_obj.get_neighbors()  # get the neighbors
            if article1_neighbors:  # if there is neighbors
                jac_dict = {}  # dictionary of index jaccard adds here

                for any_article in self.__articles_lst:
                    article2 = any_article.get_neighbors()

                    # intersection and union sets
                    union_lst= set.union(set(article1_neighbors),set(article2))
                    intersection_lst= set.intersection(set(article1_neighbors),
                                                       set(article2))
                    # calculate index jaccard
                    idx_jac = len(intersection_lst) / len(union_lst)
                    # add the name of the article and its index jaccard to dict
                    jac_dict[any_article.get_name()] = idx_jac

                sorted_list_names = []
                # The following line sorts the dictionary to a list by
                #  jaccard index (value) then by name if same values (by key)
                for key in sorted(jac_dict.items(),
                                key=lambda x: (-x[1], x[0])):
                    sorted_list_names.append(key[0])
                return sorted_list_names

    def travel_path_iterator(self, article_name):
        """
        :param article_name: name of the article
        :return: an iterator by order of the next article name in the travel
        list.
        """
        # Note: every article object has degree built in (I added a degree
        #  to every article when we create or update the network. so in this
        #   function all i have to do is just get it's degree by the get method)
        # Remember: A generator (yield) always creates an iterator
        next_article_name = article_name
        if self.__contains__(next_article_name):
            yield next_article_name
            while True:
                article_obj = self.__dict_obj[next_article_name]
                if article_obj.get_neighbors():  # if we still can travel
                    deg_dict = {}
                    sorted_deg_lst = []
                    for neighbor in article_obj.get_neighbors():
                        # add the neighbor name as key and it's degree as value
                        #  to the dictionary
                        deg_dict[neighbor.get_name()] = neighbor.get_in_deg()

                    # The following line sorts the dictionary to a list by
                    #  degree (value) then by name if same values (by key)
                    for key in sorted(deg_dict.items(), key=lambda x: (-x[1],
                                                                       x[0])):
                        sorted_deg_lst.append((key[0], key[1]))

                    # get the name of the article in the sorted list
                    next_article_name = (sorted_deg_lst[0][0])
                    yield next_article_name

                else:
                    raise StopIteration  # travel has come to an end (do not
                                         #  return more)


    def friends_helper(self, friends_set):
        """
        This is a function helper for friends_by_depth function
        :param friends_set: a set of all the current friends (object articles)
        :return: a new set that includes the new friends (neighbors of all
        the articles in the given set)
        """
        new_set = set()
        for article in friends_set:
            # add to the new set all the neighbors in the given friend set
            new_set.update(set(article.get_neighbors()))
        return new_set

    def friends_by_depth(self, article_name, depth):
        """
        :param article_name: the name of the article
        :param depth: depth of travel through friends of friends(distance)
        :return: a list of names of all the friends the article can reach in
        given distance
        """
        if self.__contains__(article_name):
            depth_x = depth
            article = self.__dict_obj[article_name]  # get the article OBJECT
            friends = set()
            friends.add(article)

            while depth_x > 0:
                new_set = self.friends_helper(friends)  # call the func helper
                # update what it returned to the friends set
                friends.update(new_set)
                depth_x -= 1

            friend_names_lst = []  # add here names of the articles in the set
            for article in friends:
                friend_names_lst.append(article.get_name())

            return friend_names_lst



link_test = read_article_links('links.txt')
net_test = WikiNetwork(link_test)

print(len(net_test.get_titles()))
result = len(net_test.friends_by_depth("History", 3))
print(result)
