val finchVersion     = "0.26.0"
val circeVersion     = "0.10.1"
val scalatestVersion = "3.0.5"

lazy val root = (project in file("."))
  .settings(
    organization := "com.amalicia",
    name := "the-wrangler",
    version := "0.0.1-SNAPSHOT",
    scalaVersion := "2.12.9",
    libraryDependencies ++= Seq(
      "com.github.finagle" %% "finchx-core"   % finchVersion,
      "com.github.finagle" %% "finchx-circe"  % finchVersion,
      "io.circe"           %% "circe-generic" % circeVersion,
      "org.scalatest"      %% "scalatest"     % scalatestVersion % "test"
    )
  )

assemblyJarName in assembly := "the-wrangler.jar"
assemblyMergeStrategy in assembly := {
  case PathList("META-INF", xs @ _*) => MergeStrategy.discard
  case x                             => MergeStrategy.first
}
