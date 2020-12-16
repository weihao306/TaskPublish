<template>
  <v-container grid-list-xs fullfilled>
    <v-toolbar dark color="blue darken-3" class="mb-1" rounded>
      <template v-show="$vuetify.breakpoint.mdAndUp">
        <v-layout row wrap justify-space-between class="mt-3">
          <v-flex xs4 sm3 md3>
            <v-menu
              ref="menu"
              v-model="menu"
              :close-on-content-click="false"
              :return-value.sync="date"
              transition="scale-transition"
              offset-y
              max-width="30rem"
              min-width="15rem"
              class="col-8"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  class="mt-2"
                  v-model="startDate"
                  placeholder="查询首日"
                  style="text-align-last: center"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker v-model="startDate" scrollable>
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="menu = false"> 取消 </v-btn>
                <v-btn text color="primary" @click="$refs.menu.save(startDate)">
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>
          </v-flex>
          <v-flex xs4 sm3 md3>
            <v-text-field
              class="mt-2"
              v-model="city"
              placeholder="城市"
              prepend-icon="mdi-city"
              style="text-align-last: center"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </v-flex>
          <v-flex xs4 sm3 md3>
            <v-select
              v-model="days"
              flat
              solo-inverted
              hide-details
              :items="selectedDays"
              @change="getStatistics(startDate, days)"
              prepend-inner-icon="mdi-magnify"
              label="查询范围日"
            >
              <template v-slot:> </template>
            </v-select>
          </v-flex>
        </v-layout>
        <!-- <v-spacer></v-spacer> -->
        <!-- <v-btn-toggle v-model="sortDesc" mandatory>
          <v-btn large depressed color="blue" :value="false">
            <v-icon>mdi-arrow-up</v-icon>
          </v-btn>
          <v-btn large depressed color="blue" :value="true">
            <v-icon>mdi-arrow-down</v-icon>
          </v-btn>
        </v-btn-toggle> -->
      </template>
    </v-toolbar>

    <v-sheet color="cyan" elevation="8" rounded>
      <v-sparkline
        :value="income.map((each) => each.costs)"
        color="rgba(255, 255, 255, .7)"
        height="150rem"
        padding="30"
        stroke-linecap="round"
        smooth
        line-width="1rem"
        auto-line-width
      >
        <!-- <template v-slot:label="item">
          {{ item.value }}￥
          {{ item.label }}
        </template> -->
        <template v-slot:label="item">
          {{ income[item.index].day }}日

          {{ income[item.index].costs }}￥
        </template>
      </v-sparkline>
    </v-sheet>
  </v-container>
</template>

<script>
export default {
  mounted() {
    // this.randDate();
  },
  computed: {
    selectedDays: () => {
      let result = new Array();
      for (let index = 1; index <= 14; index++) {
        result.push({ text: `${index}日`, value: `${index}` });
      }
      return result;
    },
  },
  data() {
    return {
      menu: false,
      city: null,
      startDate: null,
      days: null,
      income: [
        { day: 11, costs: 423 },
        { day: 12, costs: 446 },
        { day: 13, costs: 675 },
        { day: 14, costs: 510 },
        { day: 15, costs: 590 },
        { day: 16, costs: 610 },
        { day: 17, costs: 760 },
      ],
    };
  },
  methods: {
    randDate() {
      let tt = Date.now();
      for (let each of this.income) {
        let rt = new Date((tt + Math.random() * tt) / 2).getDate();
        this.date.push(rt);
      }
    },
    getStatistics(startDate, city, days) {
      this.axios
        .get("api/statistics", {
          params: { startDate: startDate, city: city, days: days },
        })
        .then((res) => {
          if (res.status === 200) {
            console.log(res);
            resData = res.data;
            this.income = [];
            for (let each of resData) {
              this.income.push(each);
            }
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style>
</style>