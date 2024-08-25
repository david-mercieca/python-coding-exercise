from domain.model.cable import Cable

#Author: David Mercieca
class Splitter:

    def __validate(self):
        valid = True
        #rules
        min_times = 1
        max_times = 64
        min_len = 2
        max_len = 1024

        if not (self.cable.length >= min_len and self.cable.length  <= max_len):
           raise ValueError("Cable Length not within required parameters")
        if not (self.times >= min_times and self.times <= max_times):
            raise ValueError("Times not within required parameters")


    def split(self, cable: Cable, times: int) -> list[Cable]:
        self.cable = cable
        self.times = times
        self.__validate()
        remaining_cable_length = cable.length
        # +1 to include the original length of cable
        total_initial_cuts = times + 1
        # even split list
        # float
        cables_list = []
        test_cables_length = remaining_cable_length / total_initial_cuts

        if remaining_cable_length % total_initial_cuts == 0:
            #even split
            cables_list = [Cable(int(remaining_cable_length / total_initial_cuts), self.generate_cable_name(n)) for n in range(total_initial_cuts)]
        else:
            cut_len =   remaining_cable_length / total_initial_cuts
            cuts_list = self.get_cuts(total_initial_cuts,cut_len)
            cables_list = ([Cable(int(cuts_list[n]), self.generate_cable_name(n)) for n in range(len(cuts_list))])
        return cables_list

    # generates the master list of main custs off offcuts (leftovers)
    def get_cuts(self, total_initial_cuts,cut_len) -> list:
        cut_len_list = []
        remainders_list = []
        remainder_cuts_list = []

        for i in range(total_initial_cuts):
            int_cut_len = int(cut_len)
            cut_len_list.append(int_cut_len)
            remainder_len = cut_len - int_cut_len
            remainders_list.append(remainder_len)

        remainder_len = sum(remainders_list)
        if remainder_len >= 1:
            number_of_cuts_remaining = int(remainder_len % total_initial_cuts)
            if(remainder_len % total_initial_cuts > 0):
                remainder_cuts_list = [int(remainder_len/number_of_cuts_remaining) for n in range (number_of_cuts_remaining)]
                remainder_len = remainder_len - sum(remainder_cuts_list)
            cut_len_list.extend(remainder_cuts_list)
            return cut_len_list
        else:
            #take another pass decrementing the cut length by 1 if the cut length can be deprecated to a min integer of 1
            if int_cut_len - 1 >= 1:
                #recursive call
                self.get_cuts(total_initial_cuts, int_cut_len - 1)
                remainders_list.append(remainder_len)
        cut_len_list.extend(remainder_cuts_list)
        return cut_len_list

    #helper method to generate cable name in correct format
    def generate_cable_name(self, idx:int)-> str:
        name_prefix = "coconuts-"
        if idx < 10:
            name_suffix = '0' + (str(idx))
        else:
            name_suffix = str(idx)
        cable_name = name_prefix + name_suffix
        return cable_name

# initialise and execute the code
initial_cable = Cable(50, "coconuts")
cable_splitter = Splitter().split(initial_cable,9)
for cable in cable_splitter:
    print("cable_name=", cable.name, "cable_len=" + str(cable.length))
