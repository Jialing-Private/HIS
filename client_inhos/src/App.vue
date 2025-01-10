<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style>

</style>

<script>
	export default{
		created() {
			if (sessionStorage.getItem("token")) {
			    this.$store.replaceState(
			        Object.assign({},this.$store.state,JSON.parse(sessionStorage.getItem("token")))
			    );
			    sessionStorage.removeItem("token")
			 }
			 
			window.addEventListener("beforeunload", () => {
			sessionStorage.setItem("token", JSON.stringify(this.$store.state));
			});
		},
	}
	
</script>
