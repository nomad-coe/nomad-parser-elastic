package eu.nomad_lab.parsers

import org.specs2.mutable.Specification

object ElasticParserSpec extends Specification {

  "ElasticParserTest" >> {
    "test with json-events" >> {
      ParserRun.parse(ElasticParser, "parsers/elastic/test/examples/elastic/INFO_ElaStic", "json-events") must_== ParseResult.ParseSuccess
    }
    "test with json" >> {
      ParserRun.parse(ElasticParser, "parsers/elastic/test/examples/elastic/INFO_ElaStic", "json") must_== ParseResult.ParseSuccess
    }

  }

}
