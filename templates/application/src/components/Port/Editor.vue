<template>
  <div class="container py-3">
    <div class="form-group">
      <label v-scope:for.title>Title</label>
      <input
          v-scope:id.title
          v-model="$proxy.state.port.title"
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
          v-model="$proxy.state.port.authenticated_wall"
          :options="walls_as_options"
          :reduce="(wall) => wall.code"
          :key="$proxy.state.port.authenticated_wall"
          :disabled="$env.state.changesLock"
      ></v-select>
      <small class="form-text">Select wall to open for authenticated users</small>
    </div>
    <div class="form-group">
      <label v-scope:for.anonymous_wall>Not authenticated user</label>
      <v-select
          class="w-100 bg-white"
          v-scope:id.anonymous_wall
          v-model="$proxy.state.port.anonymous_wall"
          :options="walls_as_options"
          :reduce="(wall) => wall.code"
          :key="$proxy.state.port.anonymous_wall"
          :disabled="$env.state.changesLock"
      ></v-select>
      <small class="form-text">Select wall to open for not authenticated users</small>
    </div>
    <div class="form-group">
      <label v-scope:for.redirect_url>Redirect URL</label>
      <input
          type="url"
          v-scope:id.redirect_url
          v-model="$proxy.state.port.redirect_url"
          :disabled="$env.state.changesLock"
          class="form-control"
      />
      <small class="form-text">If no wall specified - redirected user to this URL. </small>
    </div>
    <div class="form-group">
      <div class="d-flex align-items-center justify-content-between">
        <a :href="`/ext/${$proxy.state.port.id}/`" target="_blank" class="mr-1"> {{ url }}</a>
        <span>
          <a @click.stop.prevent="copyToClipboard(`${origin}/port/${$proxy.state.port.id}/`)" class="cursor-pointer">
            <i class="fas fa-copy mr-1 text-muted"></i>
          </a>
        <button class="btn text-success" @click="saveQR">
          <i class="fas fa-download"></i>
        </button>
        </span>
      </div>
      <div class="d-flex align-items-center flex-column m-5">
        <canvas id="port-qr" class="border"></canvas>
      </div>
    </div>
  </div>
</template>
<script>
// Front end is absolutely passive
import vSelect from "vue-select";
import {copyToClipboard, downloadImage} from "../../common"
import QRCode from "qrcode";
import proxy from "../../modules/proxy";

async function setupRoutine(to, from, next) {
  await proxy.dispatch("setPortById", to.params.portId);
  if (!proxy.state.port) {
    return next({name: "home"});
  }
  next();
}

export default {
  name: "WallOptions",
  beforeRouteEnter: setupRoutine,
  beforeRouteUpdate: setupRoutine,
  data() {
    return {
      width: 200,
      font: "Arial",
      fontSize: 14,
      margin: 4,
    };
  },
  computed: {
    canvas() {
      return document.getElementById("port-qr");
    },
    url() {
      return window.location.origin + "/port/" + this.$proxy.state.port.id + "/";
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
    ctx.fillText(this.$proxy.state.port.id, 70, height - 6);
  },
  methods: {
    copyToClipboard(text) {
      copyToClipboard(text);
      this.$notify({text: "Copied to clipboard!", type: "success"});
    },
    saveQR() {
      let dataURL = this.canvas.toDataURL("image/png");
      downloadImage(dataURL, "port_" + this.$proxy.state.port.id + ".png");
    },
  },
  components: {
    vSelect,
  },
};
</script>
