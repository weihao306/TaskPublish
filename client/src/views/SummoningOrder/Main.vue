<template>
  <v-container grid-list-xs fill-height>
    <v-layout column wrap justify-center>
      <v-flex xs6>
        <v-layout row wrap justify-center>
          <v-flex xs12 sm8 md5 lg4>
            <v-card
              class="mx-auto my-2 elevation-8"
              max-width="20rem"
              height="20rem"
              outlined
            >
              <!-- <v-card-title primary-title pt-6 style="height: 3rem" /> -->
              <v-list-item three-line>
                <v-list-item-content>
                  <v-list-item-title class="headline mb-1">
                    <v-layout row wrap justify-center>
                      <v-chip
                        class="ma-1"
                        x-large
                        label
                        color="red"
                        text-color="white"
                      >
                        <div class="text-h3 font-weight-bold">我是令主</div>
                      </v-chip>
                    </v-layout>
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-layout row wrap justify-center>
                    <v-flex xs10>
                        <blockquote class="text-justify text-h6 font-weight-bold">
                          发布和管理召集令<br/>
													邀请其他人接受召集令
                        </blockquote>
                    </v-flex>
                  </v-layout>
                </v-list-item-content>
              </v-list-item>

              <v-card-actions>
                <v-row justify="center">
                  <v-btn color="error" text-color="white" :to="{name:routerLinkName.Master}">管理召集令</v-btn>
                </v-row>
              </v-card-actions>
            </v-card>
          </v-flex>
          <v-flex xs12 sm8 md5 lg4>
            <v-card
              class="mx-auto my-2 elevation-8"
              max-width="20rem"
              height="20rem"
              outlined
            >
              <!-- <v-card-title primary-title style="height: 3rem" /> -->
              <v-list-item three-line>
                <v-list-item-content>
                  <v-list-item-title class="headline mb-1">
                    <v-layout row wrap justify-center>
                      <v-chip class="ma-1" x-large label color="primary">
                        <div class="text-h3 font-weight-bold">我是接令人</div>
                      </v-chip>
                    </v-layout>
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>

              <v-list-item>
                <v-list-item-content>
                  <v-layout row wrap justify-center>
                    <v-flex xs10>
                        <blockquote class="text-justify text-h6 font-weight-bold">
                          管理召集令<br/>
													接受召集或取消召集
                        </blockquote>
                    </v-flex>
                  </v-layout>
                </v-list-item-content>
              </v-list-item>
            
            <v-card-actions>
                <v-row justify="center">
                  <v-btn color="primary" text-color="white" :to="{name:routerLinkName.Masses}">管理召集信息</v-btn>
                </v-row>
              </v-card-actions>
            </v-card>


          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
    <!-- <v-row
      class="mb-6 d-flex"
      justify="center"
      align="center"
      justify-content="center"
    >
      <v-col cols="10" sm="6" md="5" lg="4" align-self="center">
				
			</v-col>

      <v-col cols="10" sm="6" md="5" lg="4" align-self="center">
				
			</v-col>
    </v-row> -->
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      routerLinkName: {
        Master: "Master",
        Masses: "Masses",
      },
    };
  },
  methods: {},
};
</script>

<style>
</style>