<template>
  <div class="container py-3">
    <form v-scope:id.form>
      <div class="row">
        <div class="col-12 col-md-8">
          <div class="form-group">
            <label v-scope:for.title>Title <span class="text-secondary">{{ 200 - port.title.length }}/200</span></label>
            <input
                v-scope:id.title
                v-model="port.title"
                :disabled="$env.state.changesLock"
                class="form-control"
                maxlength="200"
            />
          </div>
          <div class="form-group">
            <label v-scope:for.authenticated_wall>Authenticated user</label>
            <v-select
                class="w-100 bg-white"
                v-scope:id.authenticated_wall
                v-model="port.authenticated_wall"
                :options="walls_as_options"
                :reduce="(wall) => wall.code"
                :disabled="$env.state.changesLock"
            ></v-select>
            <small class="form-text">Select wall to open for authenticated users</small>
          </div>
          <div class="form-group">
            <label v-scope:for.anonymous_wall>Not authenticated user</label>
            <v-select
                class="w-100 bg-white"
                v-scope:id.anonymous_wall
                v-model="port.anonymous_wall"
                :options="walls_as_options"
                :reduce="(wall) => wall.code"
                :disabled="$env.state.changesLock"
            ></v-select>
            <small class="form-text">Select wall to open for not authenticated users</small>
          </div>
          <div class="form-group">
            <label v-scope:for.redirect_url>Redirect URL</label>
            <input
                type="url"
                @input="validate"
                v-scope:id.redirect_url
                v-model="port.redirect_url"
                :disabled="$env.state.changesLock"
                class="form-control"
            />
            <small class="form-text">If no wall specified - redirected user to this URL. </small>
          </div>
        </div>
        <div class="col-12 col-md-4 d-flex flex-column">
          <div class="flex-grow-1 d-flex align-items-center justify-content-center">
            <canvas id="port-qr" class="border"></canvas>
          </div>
          <div class="form-group">
            <div class="d-flex align-items-center">
              <a :href="url" target="_blank" class="flex-grow-1 mr-1 text-truncate"> {{ url }}</a>
              <a @click.stop.prevent="copyToClipboard(url)" class="cursor-pointer">
                <i class="fas fa-copy mr-1 text-muted"></i>
              </a>
              <button type="button" class="btn text-success" @click="saveQR">
                <i class="fas fa-download"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </form>
    <div class="row d-flex justify-content-end">
      <button class="btn btn-outline-danger mr-1" @click="$router.go(-1)">Close</button>
      <button class="btn btn-outline-success" @click.stop="$proxy.dispatch('updatePort', {port, warningTarget: $el})">
        Save
      </button>
    </div>
  </div>
</template>
<script>
import vSelect from "vue-select";
import {copyToClipboard, downloadImage} from "../../common"
import QRCode from "qrcode";

export default {
  data() {
    return {
      width: 200,
      font: "Arial",
      fontSize: 14,
      margin: 4,
    };
  },
  computed: {
    port() {
      return this.$store.getters.getPortById(this.$route.params.portId)
    },
    canvas() {
      return document.getElementById("port-qr");
    },
    url() {
      return window.location.origin + "/port/" + this.port.id + "/";
    },
    walls_as_options() {
      if (!this.$store.state.walls) {
        return [];
      }
      let result = [];
      for (let wall of this.$store.state.walls) {
        result.push({
          label: wall.title,
          code: wall.id,
        });
      }
      return result;
    },
  },
  mounted() {
    QRCode.toCanvas(
        this.canvas,
        this.url,
        {
          width: this.width,
          margin: this.margin,
        },
        function (error) {
          if (error) throw error;
        }
    );
    let ctx = this.canvas.getContext("2d");
    ctx.font = `${this.fontSize}px ${this.font}`;
    let height = this.canvas.height;
    let width = this.canvas.width;
    ctx.fillText(this.$store.state.app.url, width - 145, 14);
    ctx.fillText(this.port.id, 70, height - 6);
  },
  methods: {
    validate() {
      document.getElementById(this._('form')).reportValidity()
    },
    copyToClipboard(text) {
      copyToClipboard(text);
      this.$notify({text: "Copied to clipboard!", type: "success"});
    },
    saveQR() {
      let dataURL = this.canvas.toDataURL("image/png");
      downloadImage(dataURL, "port_" + this.port.id + ".png");
    },
  },
  components: {
    vSelect,
  },
};
</script>
